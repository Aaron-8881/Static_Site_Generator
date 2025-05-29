import unittest
from markdown_extract import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title_valid(self):
        markdown = "# Hello World\nSome content"
        self.assertEqual(extract_title(markdown), "Hello World")

    def test_extract_title_with_whitespace(self):
        markdown = "#   Title with spaces   \nContent"
        self.assertEqual(extract_title(markdown), "Title with spaces")

    def test_extract_title_no_h1(self):
        markdown = "## Not an h1\nContent"
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_extract_title_empty(self):
        markdown = ""
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_extract_title_multiple_lines(self):
        markdown = "Some text\n# Real Title\nMore text"
        self.assertEqual(extract_title(markdown), "Real Title")

if __name__ == "__main__":
    unittest.main()