import unittest
from markdown_converter import markdown_to_html_node
from htmlnode import ParentNode
from textnode import TextType

class TestMarkdownConverter(unittest.TestCase):
    

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )

    def test_heading(self):
        md = """
## Subheading with **bold** text

# Main heading
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>Subheading with <b>bold</b> text</h2><h1>Main heading</h1></div>",
        )

    def test_quote(self):
        md = """
> This is a _quote_ with **bold** text
> Another line
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a <i>quote</i> with <b>bold</b> text\nAnother line</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- Item with **bold**
- Item with _italic_
- Plain item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item with <b>bold</b></li><li>Item with <i>italic</i></li><li>Plain item</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. First item with `code`
2. Second item
3. Third item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item with <code>code</code></li><li>Second item</li><li>Third item</li></ol></div>",
        )

    def test_mixed_blocks(self):
        md = """
# Heading

This is a **paragraph**

```
Code block
```

> Quote with _italic_

- List item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading</h1><p>This is a <b>paragraph</b></p><pre><code>Code block</code></pre><blockquote>Quote with <i>italic</i></blockquote><ul><li>List item</li></ul></div>",
        )

    def test_empty_document(self):
        md = ""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")

    

    

if __name__ == "__main__":
    unittest.main()