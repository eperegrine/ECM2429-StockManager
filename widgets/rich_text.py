"""
A collection of methods to aid in generating kivy label markup
"""


def markup_tag(tag: str, text: str, end_tag=None) -> str:
    """
    Generates markup text for a tag

    :param tag: The tag to generate
    :param text: The text to put in the tag
    :param end_tag: Optionally change the end tag; use it to add attributes in the first tag
    :return: The markup string
    """
    end_tag = tag if end_tag is None else end_tag
    return f"[{tag}]{text}[/{end_tag}]"


def attribute_tag(tag, attribute_value, text) -> str:
    """
    Easily generate a markup tag with an attribute

    :param tag: The tag to generate
    :param attribute_value: The attribute e.g. for size: 22
    :param text: The text inside the tag
    :return: The markup string
    """
    return markup_tag(f"{tag}={attribute_value}", text, tag)


tags = {
    "BOLD": "b",
    "ITALIC": "i",
    "UNDERLINE": "i",
    "STRIKE": "s",
    "SUBSCRIPT": "sub",
    "SUPERSCRIPT": "sup"
}


def bold(text: str) -> str:
    """Generate bold markup"""
    return markup_tag("b", text)


def underline(text: str) -> str:
    """Generate underline markup"""
    return markup_tag("u", text)


def italic(text: str) -> str:
    """Generate italic markup"""
    return markup_tag("i", text)


def size(text: str, font_size: int) -> str:
    """
    Generate text size markup

    :param text: The text to markup
    :param font_size: The size of the text
    """
    return attribute_tag("size", font_size, text)


def colour(text: str, colour: str) -> str:
    """
    Generate color markup

    :param text: The text to markup
    :param colour: The colour of the text
    """
    return attribute_tag("color", colour, text)
