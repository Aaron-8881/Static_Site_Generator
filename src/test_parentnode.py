import unittest
from htmlnode import ParentNode, LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_multiple_children(self):
        children = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ]
        parent_node = ParentNode("p", children)
        self.assertEqual(
            parent_node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container", "id": "main"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container" id="main"><span>child</span></div>',
        )

    def test_to_html_no_tag_raises(self):
        child_node = LeafNode("span", "child")
        with self.assertRaises(ValueError) as context:
            ParentNode(None, [child_node])
        self.assertEqual(str(context.exception), "ParentNode must have a tag")

    def test_to_html_no_children_raises(self):
        with self.assertRaises(ValueError) as context:
            ParentNode("div", None)
        self.assertEqual(str(context.exception), "ParentNode must have a children")

    def test_to_html_empty_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_to_html_nested_parent_nodes(self):
        leaf_node = LeafNode("span", "Leaf content")
        inner_parent = ParentNode("p", [leaf_node])
        outer_parent = ParentNode("div", [inner_parent, LeafNode("b", "Bold content")])
        self.assertEqual(
            outer_parent.to_html(),
            "<div><p><span>Leaf content</span></p><b>Bold content</b></div>",
        )

if __name__ == "__main__":
    unittest.main()