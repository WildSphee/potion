design_prompt = """

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
the description can be verbose, around 20 words, compose_schema_name must be reference one that I'd provided above .
do not add extra keys / values. Try to utilize different compose_schema_name to create variety in the presentation
Do not use only one schema for the whole presentation.
do not add extra notes, start:


```json

"""

image_slide_prompt = """

```slide title
{slide_title}
```

```slide description
{slide_description}
```

convert the above title and description of a slide into a json of below format  
```json
{{
    "image_description": "<description will be passed to stable diffusion to generate a picture>",
    "slide_content": "<around 50 words of descriptions>",
}}
```

You are now generating a json to be parsed into a slide.
The image_description can be verbose, around 20 words. 
Try to create interesting pictures that depict objects and human, and nothing data / slide related. 
EG: if its a business comparison or the slide is about data, give the description of a human working on a computer instead.
EG: if its a slide about an area, company, give the description of an office building or collaborative environment instead.
Do not add extra keys / values. Do not add extra notes, start:


```json

"""
