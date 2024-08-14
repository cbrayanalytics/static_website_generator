import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        test_text = ' href="https://example.com" target="_test"'
        prop = {
            "href": "https://example.com",
            "target": "_test",
        }
        node = HTMLNode(None, None, None, prop)
        result = node.props_to_html()
        self.assertEqual(result, test_text)

    def test_props_to_html_false(self):
        test_text = ' href="https://example.com" target="_test"'
        prop = {
            "href": "https://example.com",
            "target": "_test",
        }
        prop_2 = {
            "href": "https://example.org",
            "target": "_none",
        }
        node = HTMLNode(None, None, None, prop).props_to_html()
        node2 = HTMLNode(None, None, None, prop_2).props_to_html()
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = HTMLNode(
            "a", "a string here", "children example", {"href": "https://example.com"}
        ).__repr__()
        node2 = HTMLNode(
            "a", "a string here", "children example", {"href": "https://example.com"}
        ).__repr__()
        self.assertEqual(node, node2)


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html(self):
        leaf_node1 = LeafNode("p", "This is a paragraph of text.")
        leaf_node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(leaf_node1.to_html(), "<p>This is a paragraph of text.</p>")
        self.assertEqual(
            leaf_node2.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_to_html_no_value(self):
        leaf_node1 = LeafNode("p", None, {"href": "https//www.example.com"})

        def value_none():
            nonlocal leaf_node1
            return leaf_node1.to_html()

        self.assertRaises(ValueError, value_none)


class TestParentNode(unittest.TestCase):
    ## Test multiple children
    def test_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Some bold text"),
                LeafNode(None, "Some Normal text"),
                LeafNode("i", "Some italicized text"),
            ],
        )

        self.assertEqual(
            node.to_html(),
            "<p><b>Some bold text</b>Some Normal text<i>Some italicized text</i></p>",
        )

    ## Test Nested children
    def test_nested_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Some bold text"),
                LeafNode(None, "Some Normal text"),
                ParentNode(
                    "p",
                    [
                        LeafNode(None, "Some Nested text"),
                        LeafNode("i", "Some Nested Italicized text"),
                    ],
                ),
                LeafNode("i", "Some italicized text"),
            ],
        )

        self.assertEqual(
            node.to_html(),
            "<p><b>Some bold text</b>Some Normal text<p>Some Nested text<i>Some Nested Italicized text</i></p><i>Some italicized text</i></p>",
        )

    ## Test one child
    def test_leaf_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("i", "Only this italicized text"),
            ],
        )

        self.assertEqual(
            node.to_html(),
            "<p><i>Only this italicized text</i></p>",
        )

    ## Test no children
    def test_no_children(self):
        node = ParentNode("p", None)

        def child_none():
            nonlocal node
            return node.to_html()

        self.assertRaises(ValueError, child_none)

    ## Test no tag
    def test_leaf_to_html(self):
        node = ParentNode(
            None,
            [
                LeafNode("i", "Only this italicized text"),
            ],
        )

        def tag_none():
            nonlocal node
            return node.to_html()

        self.assertRaises(ValueError, tag_none)


if __name__ == "__main__":
    unittest.main()
