import re

UPPERCASE_SEQUENCE = re.compile(r'(?!^)([A-Z]+)')

def cammel_to_snake_case(text: str) -> str:
    return UPPERCASE_SEQUENCE.sub(r'_\1', text).lower()
