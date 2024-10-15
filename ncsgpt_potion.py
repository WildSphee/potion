from typing import List

from pptx import slide

from potion import ComposeSchema, DesignSchema, Potion

# creating NCSgpt Potion from slide template


async def create_title_slide(schema: DesignSchema) -> slide:
    """Creating the title slide"""


async def create_text_slide(schema: DesignSchema) -> slide:
    """Creating the text slide"""


async def create_end_slide(schema: DesignSchema) -> slide:
    """Creating the end slide"""


compose_schemas: List[ComposeSchema] = [
    ComposeSchema(
        name="title_slide",
        desc="Use this slide when its the start of a presentation.",
        func=create_title_slide,
    ),
    ComposeSchema(
        name="text_slide",
        desc="Use this slide when you want to present a text concentrated-slide",
        func=create_text_slide,
    ),
    ComposeSchema(
        name="end_slide",
        desc="Use this slide when its the end of a presentation.",
        func=create_end_slide,
    ),
]

ncspotion = Potion(
    template_path="templates/nila_ppt_template.pptx", compose_schemas=compose_schemas
)
