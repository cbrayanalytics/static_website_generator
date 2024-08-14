import unittest

from textnode import TextNode, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)


print("Testing TextNode to HTMLNode")


class Test_TextNode_to_HTMLNode(unittest.TestCase):
    ## Test "text" type
    def test_text_type(self):
        node = TextNode("This is a text node", "text")
        print(f"Node: {node}")
        result = text_node_to_html_node(node)
        self.assertEqual(result.to_html(), "This is a text node")

    ## Test "bold" type
    def test_bold_type(self):
        node = TextNode("This is a bold node", "bold")
        result = text_node_to_html_node(node)
        self.assertEqual(result.to_html(), "<b>This is a bold node</b>")

    ## Test "italic" type
    def test_italic_type(self):
        node = TextNode("This is a italic node", "italic")
        result = text_node_to_html_node(node)
        self.assertEqual(result.to_html(), "<i>This is a italic node</i>")

    ## Test "code" type
    def test_code_type(self):
        node = TextNode("This is a code node", "code")
        result = text_node_to_html_node(node)
        self.assertEqual(result.to_html(), "<code>This is a code node</code>")

    ## Test "link" type
    def test_link_type(self):
        print("testing link_type")
        node = TextNode("This is some anchor text", "link", "http://www.example.com")
        result = text_node_to_html_node(node)
        self.assertEqual(
            result.to_html(),
            '<a href="http://www.example.com">This is some anchor text</a>',
        )

    ## Test "image" type
    def test_image_type(self):
        node = TextNode(
            "This is a photo of a butterfly", "image", "https://example.butterfly.com"
        )
        result = text_node_to_html_node(node)
        self.assertEqual(
            result.to_html(),
            '<img src="https://example.butterfly.com" alt="This is a photo of a butterfly"></img>',
        )

    ## Test failure
    def test_fail_type(self):
        node = TextNode("This is a photo of a butterfly", "fake")

        def fake_type():
            nonlocal node
            return text_node_to_html_node(node)

        self.assertRaises(Exception, fake_type)


if __name__ == "__main__":
    unittest.main()
