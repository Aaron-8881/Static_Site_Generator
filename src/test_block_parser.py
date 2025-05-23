import unittest
from block_parser import BlockType, block_to_block_type, markdown_to_blocks

class TestBlockParser(unittest.TestCase):
    def test_heading_single(self):
        text = "# Heading"
        self.assertEqual(block_to_block_type(text), BlockType.HEADING)

    def test_heading_multi_level(self):
        text = "#### Subsubsubheading"
        self.assertEqual(block_to_block_type(text), BlockType.HEADING)

    def test_heading_no_space(self):
        text = "##No space"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_code_block(self):
        text = "```\ncode here\n```"
        self.assertEqual(block_to_block_type(text), BlockType.CODE)

    def test_code_block_single_line(self):
        text = "```code```"
        self.assertEqual(block_to_block_type(text), BlockType.CODE)

    def test_code_block_not_closed(self):
        text = "```\ncode here"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_quote_block(self):
        text = "> Quote line 1\n> Quote line 2"
        self.assertEqual(block_to_block_type(text), BlockType.QUOTE)

    def test_quote_block_single_line(self):
        text = "> Single quote"
        self.assertEqual(block_to_block_type(text), BlockType.QUOTE)

    def test_quote_block_some_lines_no_quote(self):
        text = "> Quote line\nNot a quote"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        text = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(text), BlockType.UNORDERED_LIST)

    def test_unordered_list_single_item(self):
        text = "- Single item"
        self.assertEqual(block_to_block_type(text), BlockType.UNORDERED_LIST)

    def test_unordered_list_no_space(self):
        text = "-Item 1\n-Item 2"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        text = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(text), BlockType.ORDERED_LIST)

    def test_ordered_list_single_item(self):
        text = "1. Single item"
        self.assertEqual(block_to_block_type(text), BlockType.ORDERED_LIST)

    def test_ordered_list_wrong_numbering(self):
        text = "1. First item\n3. Third item"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_ordered_list_non_sequential(self):
        text = "2. First item\n3. Second item"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_ordered_list_no_space(self):
        text = "1.First item\n2.Second item"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_paragraph(self):
        text = "This is a normal paragraph."
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_paragraph_multi_line(self):
        text = "Line 1\nLine 2\nLine 3"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_empty_block(self):
        text = ""
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_mixed_content(self):
        text = "Paragraph with # heading-like text"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_single_block(self):
        md = "This is a single paragraph"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single paragraph"])

    def test_markdown_to_blocks_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_multiple_newlines(self):
        md = "First block\n\n\n\nSecond block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First block", "Second block"])

    def test_markdown_to_blocks_leading_trailing_newlines(self):
        md = "\n\nBlock 1\n\nBlock 2\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block 1", "Block 2"])

    def test_markdown_to_blocks_code_block(self):
        md = "```\ncode here\n```\n\n# Heading"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["```\ncode here\n```", "# Heading"])

    def test_markdown_to_blocks_multi_line_blocks(self):
        md = "# Heading\n\n> Quote line 1\n> Quote line 2\n\n1. Item 1\n2. Item 2"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading",
                "> Quote line 1\n> Quote line 2",
                "1. Item 1\n2. Item 2",
            ],
        )

if __name__ == "__main__":
    unittest.main()