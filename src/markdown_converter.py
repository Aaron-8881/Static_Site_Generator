from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode, TextType
from text_processor import text_to_textnodes
from node_converter import text_node_to_html_node
from block_parser import BlockType, markdown_to_blocks, block_to_block_type

def text_to_children(text):
    """Convert text with inline Markdown to a list of HTMLNodes."""
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]

def paragraph_to_html(block):
    """Convert a paragraph block to an HTMLNode."""
    children = text_to_children(block)
    return ParentNode(tag="p", children=children)

def heading_to_html(block):
    """Convert a heading block to an HTMLNode."""
    level = block.count("#", 0, block.find(" "))
    text = block.lstrip("#").strip()
    children = text_to_children(text)
    return ParentNode(tag=f"h{level}", children=children)

def code_to_html(block):
    """Convert a code block to an HTMLNode (no inline parsing)."""
    text = block.strip("```").strip()
    text_node = TextNode(text, TextType.NORMAL)
    code_node = text_node_to_html_node(text_node)
    return ParentNode(tag="pre", children=[ParentNode(tag="code", children=[code_node])])

def quote_to_html(block):
    """Convert a quote block to an HTMLNode."""
    # Remove > from each line and join
    text = "\n".join(line.lstrip(">").strip() for line in block.split("\n"))
    children = text_to_children(text)
    return ParentNode(tag="blockquote", children=children)

def unordered_list_to_html(block):
    """Convert an unordered list block to an HTMLNode."""
    items = block.split("\n")
    children = []
    for item in items:
        text = item.lstrip("-").strip()
        if text:
            item_children = text_to_children(text)
            children.append(ParentNode(tag="li", children=item_children))
    return ParentNode(tag="ul", children=children)

def ordered_list_to_html(block):
    """Convert an ordered list block to an HTMLNode."""
    items = block.split("\n")
    children = []
    for item in items:
        # Remove number and . (e.g., "1. Item" -> "Item")
        text = item[item.find(".")+1:].strip()
        if text:
            item_children = text_to_children(text)
            children.append(ParentNode(tag="li", children=item_children))
    return ParentNode(tag="ol", children=children)

def block_to_html_node(block):
    """Convert a block to an HTMLNode based on its type."""
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html(block)
    elif block_type == BlockType.HEADING:
        return heading_to_html(block)
    elif block_type == BlockType.CODE:
        return code_to_html(block)
    elif block_type == BlockType.QUOTE:
        return quote_to_html(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html(block)
    elif block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html(block)
    raise ValueError(f"Unknown block type: {block_type}")

def markdown_to_html_node(markdown):
    """Convert a Markdown document to a single parent HTMLNode."""
    blocks = markdown_to_blocks(markdown)
    block_nodes = [block_to_html_node(block) for block in blocks]
    return ParentNode(tag="div", children=block_nodes)