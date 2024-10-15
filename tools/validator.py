import re

from pathvalidate import sanitize_filename


def convert_to_filename(s: str) -> str:
    # Sanitize the string to make it a valid filename
    filename = sanitize_filename(s)
    filename = filename.replace(" ", "_")
    return filename


def trim_code_block(json_str: str) -> str:
    # remove code blocks around
    code_fence_pattern = r"^```(?:json)?\s*([\s\S]*?)\s*```$"
    match = re.match(code_fence_pattern, json_str, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return json_str.strip("`")
