from textnode import TextNode, TextType
from htmlnode import LeafNode

def text_node_to_html_node(text_node):
    if not isinstance(text_node, TextNode):
        raise ValueError("Input must be a TextNode")
    
    text_type = text_node.text_type
    text = text_node.text
    url = text_node.url

    if text_type == TextType.NORMAL:
        return LeafNode(None, text)
    elif text_type == TextType.BOLD:
        return LeafNode("b", text)
    elif text_type == TextType.ITALIC:
        return LeafNode("i", text)
    elif text_type == TextType.CODE:
        return LeafNode("code", text)
    elif text_type == TextType.LINK:
        if url is None:
            raise ValueError("Link TextNode must have a URL")
        return LeafNode("a", text, {"href": url})
    elif text_type == TextType.IMAGE:
        if url is None:
            raise ValueError("Image TextNode must have a URL")
        return LeafNode("img", "", {"src": url, "alt": text})
    else:
        raise ValueError(f"Invalid TextType: {text_type}")