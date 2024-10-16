import json
import os
from typing import Callable, Dict, List, Union

from pptx import Presentation
from pptx.presentation import Presentation as PPT
from pptx.slide import Slide
from pydantic import BaseModel, Field, TypeAdapter, ValidationError

from llms.openai import call_openai
from llms.ppt_prompt import ppt_prompt
from tools.validator import convert_to_filename, trim_code_block

"""Logic Flow

user input a query - eg: "design a ppt about goose"

LLM first generates a list of DesignSchema, giving each slide a title, a description of their content, and their compose_schema_name

for each DesignSchema (slide), get their corresponding func from ComposeSchema, input the desc and title into it, and ask it to generate a PPT. 

gather all async func results, compose them into one single PPT

Returns a path to the PPT
"""


class DesignSchema(BaseModel):
    """
    This BaseModel is used for each slide during the design phase
    """

    slide_title: str = Field(..., description="Name of the slide, eg: flowchart")
    desc: str = Field(
        ...,
        description="Description to when to use this slide, eg: to create a flowchart to represent time series events",
    )
    compose_schema_name: str = Field(
        ..., description="name of the compose schema to be used"
    )


class ComposeSchema(BaseModel):
    """
    This BaseModel is used for each slide during the compose phase
    """

    name: str = Field(..., description="Name of the slide, eg: flowchart")
    desc: str = Field(
        ...,
        description="When to use this slide, eg: to create a flowchart to represent time series events",
    )
    func: Callable = Field(
        ...,
        description="Function to input the schema and create the slide, returns a pptx slide obj",
    )
    slide_layout_index: int = Field(
        ..., description="which slide layout to use for each slide type"
    )


class Potion:
    def __init__(
        self, template_path: str, compose_schemas: List[ComposeSchema]
    ) -> None:
        self.template_path: str = template_path
        self.compose_schemas: List[ComposeSchema] = compose_schemas

        self.presentation = Presentation(template_path)
        self.ppt_length: int = len(self.presentation.slides)

    def _create_compose_schema_desc(self) -> str:
        """Create a str interpretation of all the compose schemas"""
        res = "**************\n"
        for schema in self.compose_schemas:
            res += f"compose_schema_name: {schema.name}\n"
            res += f"when to call it: {schema.desc}\n"
            res += "**************\n"
        return res

    def design(self, query: str, attempts: int = 2) -> Union[List[DesignSchema], Dict]:
        """From the user description, create a JSON output of the PowerPoint"""

        # call to OpenAI API to create the Design Schema
        json_str = call_openai(
            ppt_prompt.format(
                ppt_outline=query, compose_schema=self._create_compose_schema_desc()
            )
        )
        json_str = trim_code_block(json_str)
        print(f"Created JSON outline, original: \n{query}\n\n after:\n{json_str}")

        try:
            # load the output into List[DesignSchema] format and return it
            json_outline = json.loads(json_str)
            adapter = TypeAdapter(List[DesignSchema])
            return adapter.validate_python(json_outline)

        except (json.JSONDecodeError, ValidationError) as e:
            # if the json parsing failed or casting to List[DesignSchema] fails, recursively retry again
            if attempts > 0:
                return self.design(query, attempts - 1)

            # Return error details after all attempts fail
            error_type = (
                "Invalid JSON format"
                if isinstance(e, json.JSONDecodeError)
                else "Validation error"
            )
            return {"error": error_type, "details": str(e)}

    def duplicate_slide(self, slide_index: int) -> Slide:
        """
        Duplicate a slide from the presentation.

        Args:
            prs: The PowerPoint presentation object.
            slide_index: The index of the slide to duplicate.

        Returns:
            The new slide that is a duplicate of the original one.
        """
        presentation: PPT = self.presentation
        original_slide = presentation.slides[slide_index]
        slide_layout = original_slide.slide_layout
        new_slide = presentation.slides.add_slide(slide_layout)

        for shape in original_slide.shapes:
            # Check if the shape has text and duplicate it
            if shape.has_text_frame:
                new_shape = new_slide.shapes.add_textbox(
                    shape.left, shape.top, shape.width, shape.height
                )
                new_shape.text_frame.text = shape.text_frame.text
                for paragraph, new_paragraph in zip(
                    shape.text_frame.paragraphs, new_shape.text_frame.paragraphs
                ):
                    new_paragraph.font.size = paragraph.font.size
                    new_paragraph.font.bold = paragraph.font.bold

            # Check if the shape is an image and duplicate it
            elif shape.shape_type == 13:  # MSO_SHAPE_TYPE.PICTURE
                image_stream = shape.image.blob
                new_slide.shapes.add_picture(
                    image_stream, shape.left, shape.top, shape.width, shape.height
                )

            # Check for other shapes and handle accordingly
            elif shape.shape_type in [1, 3]:  # AutoShape or Placeholder
                new_slide.shapes.add_shape(
                    shape.auto_shape_type,
                    shape.left,
                    shape.top,
                    shape.width,
                    shape.height,
                )

        return new_slide

    async def compose(self, design_schemas: List[DesignSchema]) -> None:
        """Create the PPTX based on the design schema list"""

        for ds in design_schemas:
            # Find the corresponding ComposeSchema
            compose_schema = None
            for cs in self.compose_schemas:
                if cs.name == ds.compose_schema_name:
                    compose_schema = cs

            if compose_schema is None:
                continue

            slide: Slide = self.presentation.slides[compose_schema.slide_layout_index]

            print("COMPOSING", ds, compose_schema)

            # Duplicate target slide
            slide = self.duplicate_slide(compose_schema.slide_layout_index)
            # Add a new slide based on the layout
            # self.presentation.slides.add_slide(slide)

            # Call the compose function to modify the slide
            await compose_schema.func(ds, slide)

    def save(self) -> os.PathLike:
        filename = convert_to_filename("output")
        output_path: os.PathLike = (
            f'{os.getenv("PPT_OUTPUT_FOLDER") or "output/"}{filename}.pptx'
        )
        self.presentation.save(output_path)

        return output_path
