import re

def extract_number(pattern, text):
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).replace(",", "")
    return None
