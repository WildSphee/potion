from pathvalidate import sanitize_filename


def convert_to_filename(s):
    # Sanitize the string to make it a valid filename
    filename = sanitize_filename(s)
    filename = filename.replace(" ", "_")
    return filename
