import os
import uuid
from typing import Optional
from fastapi import HTTPException
from replicate.exceptions import ModelError
import replicate
import requests

async def create_image(
    prompt: Optional[str] = "Singaporeans working in an office, collaborating, on computer, desk, high resolution, field of depth."
) -> str:
    input_params = {
        "prompt": prompt,
        "go_fast": True,
        "guidance": 3.5,
        "megapixels": "1",
        "num_outputs": 1,
        "prompt_strength": 0.8,
        "num_inference_steps": 28,
        "aspect_ratio": "1:1",
        "output_format": "jpg",
        "output_quality": 80,
    }

    try:
        # Run the model to get the output URL
        output = await replicate.async_run("black-forest-labs/flux-pro", input=input_params)
    except ModelError as e:
        raise HTTPException(status_code=500, detail=f"Replicate Generation Error: {e}")

    # Construct the full path for the output file
    output_path = os.path.join("output", f"{str(uuid.uuid4())}.jpg")

    # Download the image synchronously and save it
    try:
        response = requests.get(output, stream=True)
        if response.status_code == 200:
            os.makedirs("templates", exist_ok=True)  # Ensure the output folder exists
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        else:
            raise HTTPException(status_code=500, detail="Failed to download the image.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image download error: {e}")

    return output_path
