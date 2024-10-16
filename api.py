from typing import List, Literal

from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse

from ncsgpt_potion import ncspotion
from potion import DesignSchema

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

    # saving the PPT
    path = ncspotion.save(design[0].desc)

    return FileResponse(
        path,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
    )
