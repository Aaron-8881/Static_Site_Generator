from textnode import TextNode, TextType
from markdown_extract import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        if not node.text:
            new_nodes.append(node)
            continue
        
        # Split text on delimiter
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid Markdown syntax: missing closing delimiter '{delimiter}'")
        
        # Process parts, alternating between NORMAL and specified text_type
        for i, part in enumerate(parts):
            if not part:
                continue  # Skip empty parts
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.NORMAL))
            else:
                new_nodes.append(TextNode(part, text_type))
    
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        if not node.text:
            new_nodes.append(node)
            continue
        
        text = node.text
        images = extract_markdown_images(text)
        if not images:
            new_nodes.append(node)
            continue
        
        for alt_text, url in images:
            # Split on the image markdown, max one split
            markdown = f"![{alt_text}]({url})"
            before, after = text.split(markdown, 1)
            if before:
                new_nodes.append(TextNode(before, TextType.NORMAL))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            text = after
        
        if text:
            new_nodes.append(TextNode(text, TextType.NORMAL))
    
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        if not node.text:
            new_nodes.append(node)
            continue
        
        text = node.text
        links = extract_markdown_links(text)
        if not links:
            new_nodes.append(node)
            continue
        
        for anchor_text, url in links:
            # Split on the link markdown, max one split
            markdown = f"[{anchor_text}]({url})"
            before, after = text.split(markdown, 1)
            if before:
                new_nodes.append(TextNode(before, TextType.NORMAL))
            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
            text = after
        
        if text:
            new_nodes.append(TextNode(text, TextType.NORMAL))
    
    return new_nodes

def text_to_textnodes(text):
    # Start with a single NORMAL node
    nodes = [TextNode(text, TextType.NORMAL)]
    
    # Apply splitting functions in order
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes