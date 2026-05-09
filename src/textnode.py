from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str|None = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: object) -> bool:
        if not type(other) == TextNode:
            return False
        return self.text == other.text \
                and self.text_type == other.text_type \
                and self.url == other.url

    def __repr__(self) -> str:
        return f"TextNode(text: {self.text}, type: {self.text_type.value}, url: {self.url})"
