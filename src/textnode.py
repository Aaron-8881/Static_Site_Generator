from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (self.text == other.text and
                self.text_type == other.text_type and
                self.url == other.url)
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
    def text_node_to_html_node(text_node):
        if not isinstance(text_node, TextNode):
            raise ValueError("Expected a TextNode")
        if text_node.text_type == TextType.NORMAL:
            return LeafNode(tag=None, value=text_node.text)
        elif text_node.text_type == TextType.BOLD:
            return LeafNode(tag="strong", value=text_node.text)
        elif text_node.text_type == TextType.ITALIC:
            return LeafNode(tag="em", value=text_node.text)
        elif text_node.text_type == TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        elif text_node.text_type == TextType.LINK:
            if text_node.url is None:
                raise ValueError("URL must be provided for link text type")
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        elif text_node.text_type == TextType.IMAGE:
            if text_node.url is None:
                raise ValueError("URL must be provided for image text type")
            return LeafNode(tag="img", value=None, props={"src": text_node.url, "alt": text_node.text})
        else:
            raise ValueError(f"Unknown text type: {text_node.text_type}")
        
        
