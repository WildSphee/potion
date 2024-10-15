ppt_prompt = """

```PPT outline
{ppt_outline}
```

convert the above powerpoint outline into json format like below:

{{
    "title": "Insert Title Here",
    "slides": [
        {{
            "page": 1,
            "header": "One line header description",
            "content": "verbose summary / bulletpoints"
        }},
        {{
            "page": 2,
            "header": "One line header description",
            "content": "verbose summary / bulletpoints"
        }},
        {{
            "page": 3,
            "header": "One line header description",
            "content": "verbose summary / bulletpoints"
        }},
        {{
            "page": 4,
            "header": "One line header description",
            "content": "verbose summary / bulletpoints"
        }}
        ...
    ]
}}

the powerpoint can have up to 10 slides, all in json format stated above, the title can only be 3 words or less
the content can only be str, point, do not add extra keys / values
do not add extra notes:

```json


"""
