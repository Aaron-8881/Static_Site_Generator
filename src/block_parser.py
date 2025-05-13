from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(text):
    if not text:
        return BlockType.PARAGRAPH
    
    lines = text.split("\n")
    
    # Check for heading: starts with 1-6 # followed by space
    if re.match(r"^#{1,6}\s", text):
        return BlockType.HEADING
    
    # Check for code: starts and ends with triple backticks
    if text.startswith("```") and text.endswith("```"):
        return BlockType.CODE
    
    # Check for quote: every line starts with >
    if all(line.startswith(">") for line in lines if line):
        return BlockType.QUOTE
    
    # Check for unordered list: every line starts with - followed by space
    if all(line.startswith("- ") for line in lines if line):
        return BlockType.UNORDERED_LIST
    
    # Check for ordered list: lines start with 1., 2., etc., incrementing from 1
    if lines and all(line.strip() for line in lines):
        ordered = True
        for i, line in enumerate(lines, 1):
            if not re.match(rf"^{i}\.\s", line):
                ordered = False
                break
        if ordered:
            return BlockType.ORDERED_LIST
    
    # Default to paragraph
    return BlockType.PARAGRAPH