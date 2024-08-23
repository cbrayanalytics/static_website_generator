import unittest

from textnode import TextNode
from splitnode import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
)

text_type_text = "text"
text_type_bold = "bold"
text_type_code = "code"
text_type_italic = "italic"


class TestTextNode(unittest.TestCase):
    ## Test bold
    def test_bold(self):
        node = TextNode("This is a **text** node", text_type_text)
        split_node = split_nodes_delimiter([node], "**", text_type_bold)

        result = [
            TextNode("This is a ", "text"),
            TextNode("text", "bold"),
            TextNode(" node", "text"),
        ]

        self.assertEqual(split_node, result)

    ## Test Italic
    def test_italic(self):
        node = TextNode("This is a *text* node", text_type_text)
        split_node = split_nodes_delimiter([node], "*", text_type_italic)

        result = [
            TextNode("This is a ", "text"),
            TextNode("text", "italic"),
            TextNode(" node", "text"),
        ]

        self.assertEqual(split_node, result)

    ## Test code
    def test_code(self):
        node = TextNode("This is a `text` node", text_type_text)
        split_node = split_nodes_delimiter([node], "`", text_type_code)

        result = [
            TextNode("This is a ", "text"),
            TextNode("text", "code"),
            TextNode(" node", "text"),
        ]

        self.assertEqual(split_node, result)

    ## Test Node that is not of text_type text
    def test_non_text(self):
        node = TextNode("This is a `text` node", text_type_code)
        split_node = split_nodes_delimiter([node], "`", text_type_code)

        result = [TextNode("This is a `text` node", "code")]

        self.assertEqual(split_node, result)

    #
    # Test Inavlid md
    def test_invalid_md(self):
        node = TextNode("This is a photo of a butterfly", text_type_text)

        def invalid_md():
            nonlocal node
            return split_nodes_delimiter([node], "&", text_type_code)

        self.assertRaises(Exception, invalid_md)

    # Test single delimiter
    def test_single_del(self):
        node = TextNode("This is a 'photo of a butterfly", text_type_text)

        def invalid_md():
            nonlocal node
            return split_nodes_delimiter([node], "'", text_type_code)

        self.assertRaises(Exception, invalid_md)

    ## Test extract_markdown_links
    def test_extract_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        test = extract_markdown_links(text)
        result = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]

        self.assertEqual(test, result)

    ## Test extract_markdown_images
    def test_extract_image(self):
        text = "This is a text with ![rowdy piper](https://example.org/first-time) and ![second roudn](https://example.org/second-time)"
        test = extract_markdown_images(text)
        result = [
            ("rowdy piper", "https://example.org/first-time"),
            ("second roudn", "https://example.org/second-time"),
        ]

        self.assertEqual(test, result)


if __name__ == "__main__":
    unittest.main()
