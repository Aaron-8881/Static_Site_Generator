import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_multiple_props(self):
        # Testing props_to_html with multiple attributes
        node = HTMLNode(
            tag="a",
            value="Click me",
            props={"href": "https://www.google.com", "target": "_blank"}
        )
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_with_empty_props(self):
        # Testing props_to_html with no attributes
        node = HTMLNode(tag="p", value="Paragraph text")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_single_prop(self):
        # Testing props_to_html with one attribute
        node = HTMLNode(tag="img", props={"src": "image.jpg"})
        self.assertEqual(node.props_to_html(), ' src="image.jpg"')

    def test_to_html_raises_not_implemented(self):
        # Testing that to_html raises NotImplementedError
        node = HTMLNode(tag="div")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr(self):
        # Testing the __repr__ method
        node = HTMLNode(
            tag="a",
            value="Link",
            children=[HTMLNode(tag="span")],
            props={"href": "https://example.com"}
        )
        expected = "HTMLNode(tag=a, value=Link, children=[HTMLNode(tag=span, value=None, children=[], props={})], props={'href': 'https://example.com'})"
        self.assertEqual(repr(node), expected)

if __name__ == "__main__":
    unittest.main()