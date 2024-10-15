import json
import os
from typing import Callable, Dict, List, Union

from pptx import Presentation
from pydantic import BaseModel, Field, TypeAdapter, ValidationError

from llms.openai import call_openai
from llms.ppt_prompt import ppt_prompt
from tools.validator import trim_code_block
from typing import Callable, Optional
import asyncio

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

    async def compose(self, design_schema: List[DesignSchema]) -> os.PathLike:
        """Create the PPTX base on requirement"""

        tasks: List = []

        for ds in design_schema:
            # get the corresponding ComposeSchema
            cs: Optional[ComposeSchema] = next((cs for cs in self.compose_schemas if cs.name == ds.compose_schema_name), None)
            func: Callable = cs.func
            tasks.append(asyncio.create_task(func(ds)))


        results: List = await asyncio.gather(*tasks)
        