import re


def camel_to_snake(string: str) -> str:
    """Turns `SOMEMeaningfulText` into `some_meaningful_text`"""
    result = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", string)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", result).lower()
