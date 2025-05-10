import unittest
from textnode import TextNode, TextType
from text_processor import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes

class TestTextProcessor(unittest.TestCase):
    def test_split_delimiter_code_single(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.NORMAL),
        ]
        self.assertListEqual(expected, result)

    def test_split_delimiter_bold_single(self):
        node = TextNode("This is **bold** text", TextType.NORMAL)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.NORMAL),
        ]
        self.assertListEqual(expected, result)

    def test_split_delimiter_italic_single(self):
        node = TextNode("This is _italic_ text", TextType.NORMAL)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.NORMAL),
        ]
        self.assertListEqual(expected, result)

    def test_split_delimiter_multiple_delimiters(self):
        node = TextNode("This is `code1` and `code2` text", TextType.NORMAL)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("code1", TextType.CODE),
            TextNode(" and ", TextType.NORMAL),
            TextNode("code2", TextType.CODE),
            TextNode(" text", TextType.NORMAL),
        ]
        self.assertListEqual(expected, result)

    def test_split_delimiter_non_text_node(self):
        node1 = TextNode("Bold text", TextType.BOLD)
        node2 = TextNode("This is `code` text", TextType.NORMAL)
        result = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        expected = [
            TextNode("Bold text", TextType.BOLD),
            TextNode("This is ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.NORMAL),
        ]
        self.assertListEqual(expected, result)

    def test_split_delimiter_no_delimiter(self):
        node = TextNode("Plain text", TextType.NORMAL)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("Plain text", TextType.NORMAL)]
        self.assertListEqual(expected, result)

    def test_split_delimiter_missing_closing_delimiter(self):
        node = TextNode("This is `code text", TextType.NORMAL)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(str(context.exception), "Invalid Markdown syntax: missing closing delimiter '`'")

    def test_split_delimiter_empty_text(self):
        node = TextNode("", TextType.NORMAL)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("", TextType.NORMAL)]
        self.assertListEqual(expected, result)

    def test_split_delimiter_at_start(self):
        node = TextNode("`code` text", TextType.NORMAL)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.NORMAL),
        ]
        self.assertListEqual(expected, result)

    def test_split_delimiter_at_end(self):
        node = TextNode("text `code`", TextType.NORMAL)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("text ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
        ]
        self.assertListEqual(expected, result)

    

    def test_split_delimiter_multiple_nodes(self):
        nodes = [
            TextNode("This is **bold** text", TextType.NORMAL),
            TextNode("Plain text", TextType.NORMAL),
            TextNode("Italic text", TextType.ITALIC),
        ]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.NORMAL),
            TextNode("Plain text", TextType.NORMAL),
            TextNode("Italic text", TextType.ITALIC),
        ]
        self.assertListEqual(expected, result)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_single(self):
        node = TextNode(
            "Text with ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images_no_images(self):
        node = TextNode("Plain text", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("Plain text", TextType.NORMAL)], new_nodes)

    def test_split_images_non_text_node(self):
        node1 = TextNode("Bold text", TextType.BOLD)
        node2 = TextNode(
            "Text with ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node1, node2])
        self.assertListEqual(
            [
                TextNode("Bold text", TextType.BOLD),
                TextNode("Text with ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images_empty_text(self):
        node = TextNode("", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("", TextType.NORMAL)], new_nodes)

    def test_split_images_at_start(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) text",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" text", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_split_images_at_end(self):
        node = TextNode(
            "text ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("text ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.NORMAL),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.NORMAL),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_split_links_single(self):
        node = TextNode(
            "Text with [link](https://www.boot.dev)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_split_links_no_links(self):
        node = TextNode("Plain text", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("Plain text", TextType.NORMAL)], new_nodes)

    def test_split_links_non_text_node(self):
        node1 = TextNode("Italic text", TextType.ITALIC)
        node2 = TextNode(
            "Text with [link](https://www.boot.dev)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node1, node2])
        self.assertListEqual(
            [
                TextNode("Italic text", TextType.ITALIC),
                TextNode("Text with ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_split_links_empty_text(self):
        node = TextNode("", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("", TextType.NORMAL)], new_nodes)

    def test_split_links_at_start(self):
        node = TextNode(
            "[link](https://www.boot.dev) text",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" text", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_split_links_at_end(self):
        node = TextNode(
            "text [link](https://www.boot.dev)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("text ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

   

    def test_split_links_mixed_content(self):
        node = TextNode(
            "Text with ![image](https://i.imgur.com/zjjcJKZ.png) and [link](https://www.boot.dev)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text with ![image](https://i.imgur.com/zjjcJKZ.png) and ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_mixed(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.NORMAL),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_only_bold(self):
        text = "This is **bold** text"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.NORMAL),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_only_image(self):
        text = "![image](https://i.imgur.com/zjjcJKZ.png)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_plain_text(self):
        text = "Plain text"
        nodes = text_to_textnodes(text)
        expected = [TextNode("Plain text", TextType.NORMAL)]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_empty(self):
        text = ""
        nodes = text_to_textnodes(text)
        expected = [TextNode("", TextType.NORMAL)]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_multiple_types(self):
        text = "**bold** _italic_ `code`"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_invalid_delimiter(self):
        text = "This is `code text"
        with self.assertRaises(ValueError) as context:
            text_to_textnodes(text)
        self.assertEqual(str(context.exception), "Invalid Markdown syntax: missing closing delimiter '`'")
