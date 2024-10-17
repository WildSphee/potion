from typing import List, Literal

from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse

from llms.openai import call_openai
from ncsgpt_potion import ncspotion
from potion import DesignSchema
from tools.validator import convert_to_filename

app = FastAPI()


@app.post("/create-ppt/")
async def create_file(
    content: str = Form(...), template: Literal["NILA"] = "NILA"
) -> FileResponse:
    potion = None
    if template == "NILA":
        potion = ncspotion

    if potion is None:
        raise HTTPException(status_code=400, detail="No template matched.")

    # creating a design schema
    design: List[DesignSchema] = await ncspotion.design(content, 1)

    # creating the PPT
    await ncspotion.compose(design)

    # create filename
    filename = await call_openai(f'Generate a filename for a powerpoint base on the the \
        description: \n\******\n{content}\n******\n\
        do not include " or quotes blocks. Make it 3 words or less. like "AWS vs Azure": ')
    filename = convert_to_filename(filename)

    # saving the PPT
    path = ncspotion.save(filename)

    return FileResponse(
        path,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
    )
