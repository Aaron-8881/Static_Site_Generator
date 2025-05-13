import unittest
from block_parser import BlockType, block_to_block_type

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

if __name__ == "__main__":
    unittest.main()