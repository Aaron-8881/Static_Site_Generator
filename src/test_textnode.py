import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("Link text", TextType.LINK, "https://boot.dev")
        node2 = TextNode("Link text", TextType.LINK, "https://boot.dev")
        self.assertEqual(node, node2)

    def text_not_eq_different_text(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_url(self):
        node = TextNode("Link text", TextType.LINK, "https://boot.dev")
        node2 = TextNode("Link text", TextType.LINK, "https://freecodecamp.org")
        self.assertNotEqual(node, node2)

    def test_eq_none_url(self):
        node = TextNode("This is a test node", TextType.LINK, None)
        node2 = TextNode("This is a text node", TextType.LINK, None)



if __name__ == "__main__":
    unittest.main()