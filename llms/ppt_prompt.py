ppt_prompt = """

```PPT outline
{ppt_outline}
```

```compose schema
{compose_schema}
```


convert the above powerpoint outline into json list format like below:
```json
[
    {{
        "slide_title": "",
        "desc": "",
        "compose_schema_name": ""
    }},
    ...
]
```

the powerpoint can have up to 10 slides, all in json format stated above, the title can only be 3 words or less
the description can be verbose, around 15 words, compose_schema_name must be reference one that I'd provided above .
do not add extra keys / values
do not add extra notes, start:


```json

"""
