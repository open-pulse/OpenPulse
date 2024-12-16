import re

UPPERCASE_SEQUENCE = re.compile(r"(?!^)([A-Z]+)")


def pascal_to_snake_case(text: str) -> str:
    return UPPERCASE_SEQUENCE.sub(r"_\1", text).lower()


def pascal_to_spaced_case(text: str) -> str:
    return UPPERCASE_SEQUENCE.sub(r" \1", text)
