import uuid
from typing import List, Literal

from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse

from ncsgpt_potion import compose_schemas as ncs_compose_schemas
from potion import DesignSchema, Potion
from tools.validator import convert_to_filename

app = FastAPI()


@app.post("/create-ppt/")
async def create_file(
    content: str = Form(...), template: Literal["NCSGPT"] = "NCSGPT"
) -> FileResponse:
    potion = None
    if template == "NCSGPT":
        potion = Potion(
            template_path="templates/nila_ppt_template.pptx",
            compose_schemas=ncs_compose_schemas,
        )

    if potion is None:
        raise HTTPException(status_code=400, detail="No template matched.")

    # creating a design schema
    design: List[DesignSchema] = await potion.design(content, 1)

    # creating the PPT
    await potion.compose(design)

    # create filename
    # filename = await call_openai(f'Generate a filename for a powerpoint base on the the \
    #     description: \n\******\n{content}\n******\n\
    #     do not include " or quotes blocks. Make it 3 words or less. like "AWS vs Azure": ')
    filename = convert_to_filename(str(uuid.uuid4()))

    # saving the PPT
    path = potion.save(filename)

    return FileResponse(
        path,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
    )
