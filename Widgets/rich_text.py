def markup_tag(tag, text, end_tag=None):
    end_tag = tag if end_tag is None else end_tag
    return f"[{tag}]{text}[/{end_tag}]"


def attribute_tag(tag, attribute_value, text):
    return markup_tag(f"{tag}={attribute_value}", text, tag)


tags = {
    "BOLD": "b",
    "ITALIC": "i",
    "UNDERLINE": "i",
    "STRIKE": "s",
    "SUBSCRIPT": "sub",
    "SUPERSCRIPT": "sup"
}


def bold(text):
    return markup_tag("b", text)


def underline(text):
    return markup_tag("u", text)


def italic(text):
    return markup_tag("i", text)


def size(text, font_size: int):
    return attribute_tag("size", font_size, text)


def colour(text, colour: str):
    return attribute_tag("color", colour, text)
