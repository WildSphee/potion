import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def call_openai(query: str = "") -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    messages = [
        {"role": "user", "content": query},
    ]

    completion = client.chat.completions.create(
        temperature=0.2,
        model="gpt-4o-mini",
        messages=messages,
    )

    res: str = completion.choices[0].message.content
    return res
