import re

from pathvalidate import sanitize_filename


def convert_to_filename(s):
    # Sanitize the string to make it a valid filename
    filename = sanitize_filename(s)
    filename = filename.replace(" ", "_")
    return filename


def trim_code_block(json_str):
    # Use regex to remove ```json and ``` if they exist
    pattern = r"^```json\s*(.*?)\s*```$"
    match = re.match(pattern, json_str, re.DOTALL)
    if match:
        return match.group(1).strip()
    return json_str
