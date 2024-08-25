import unittest

from textnode import TextNode
from splitnode import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_images,
    split_nodes_links,
)

text_type_text = "text"
text_type_bold = "bold"
text_type_code = "code"
text_type_italic = "italic"
text_type_image = "image"
text_type_link = "link"


class TestSplitNode(unittest.TestCase):
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

    # Test single delimiter
    def test_single_del(self):
        node = TextNode("This is a 'photo of a butterfly", text_type_text)

        def invalid_md():
            nonlocal node
            return split_nodes_delimiter([node], "'", text_type_code)

        self.assertRaises(Exception, invalid_md)

    #### extract_markdown_images

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

    ## Test split_node_images default
    def test_split_node_images(self):
        node = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            text_type_text,
        )

        test = split_nodes_images([node])

        result = [
            TextNode("This is text with a link ", text_type_text),
            TextNode("to boot dev", text_type_image, "https://www.boot.dev"),
            TextNode(" and ", text_type_text),
            TextNode(
                "to youtube", text_type_image, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(test, result)

    ## Test split_node_images with multiple input nodes.
    def test_split_node_multiple_images(self):
        node = [
            TextNode(
                "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
                text_type_text,
            ),
            TextNode(
                "This is a second link ![to boot dev](https://www.boot.org) and ![youtube](https://www.youtube.com/@bootdotdev)",
                text_type_text,
            ),
        ]

        test = split_nodes_images(node)

        result = [
            TextNode("This is text with a link ", text_type_text),
            TextNode("to boot dev", text_type_image, "https://www.boot.dev"),
            TextNode(" and ", text_type_text),
            TextNode(
                "to youtube", text_type_image, "https://www.youtube.com/@bootdotdev"
            ),
            TextNode("This is a second link ", text_type_text),
            TextNode("to boot dev", text_type_image, "https://www.boot.org"),
            TextNode(" and ", text_type_text),
            TextNode("youtube", text_type_image, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(test, result)

    ## Test split_node_images with image first
    def test_split_node_images_backwards(self):
        node = TextNode(
            "![to boot](https://www.boot.dev) That was a link ![to youtube](https://www.youtube.com/@bootdotdev) here is another.",
            text_type_text,
        )

        test = split_nodes_images([node])

        result = [
            TextNode("to boot", text_type_image, "https://www.boot.dev"),
            TextNode(" That was a link ", text_type_text),
            TextNode(
                "to youtube", text_type_image, "https://www.youtube.com/@bootdotdev"
            ),
            TextNode(" here is another.", text_type_text),
        ]
        self.assertEqual(test, result)

    def test_split_node_no_images(self):
        node = TextNode(
            "[to boot](https://www.boot.dev) That was a link [to youtube](https://www.youtube.com/@bootdotdev) here is another.",
            text_type_text,
        )

        test = split_nodes_images([node])

        result = [
            TextNode(
                "[to boot](https://www.boot.dev) That was a link [to youtube](https://www.youtube.com/@bootdotdev) here is another.",
                text_type_text,
            )
        ]
        self.assertEqual(test, result)

    #### split_node_links

    ## Test split_node_links default
    def test_split_node_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            text_type_text,
        )

        test = split_nodes_links([node])

        result = [
            TextNode("This is text with a link ", text_type_text),
            TextNode("to boot dev", text_type_link, "https://www.boot.dev"),
            TextNode(" and ", text_type_text),
            TextNode(
                "to youtube", text_type_link, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(test, result)

    ## Test split_node_links with multiple input nodes.
    def test_split_node_multiple_links(self):
        node = [
            TextNode(
                "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                text_type_text,
            ),
            TextNode(
                "This is a second link [to boot dev](https://www.boot.org) and [youtube](https://www.youtube.com/@bootdotdev)",
                text_type_text,
            ),
        ]

        test = split_nodes_links(node)

        result = [
            TextNode("This is text with a link ", text_type_text),
            TextNode("to boot dev", text_type_link, "https://www.boot.dev"),
            TextNode(" and ", text_type_text),
            TextNode(
                "to youtube", text_type_link, "https://www.youtube.com/@bootdotdev"
            ),
            TextNode("This is a second link ", text_type_text),
            TextNode("to boot dev", text_type_link, "https://www.boot.org"),
            TextNode(" and ", text_type_text),
            TextNode("youtube", text_type_link, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(test, result)

    ## Test split_node_links with link first
    def test_split_node_links_backwards(self):
        node = TextNode(
            "[to boot](https://www.boot.dev) That was a link [to youtube](https://www.youtube.com/@bootdotdev) here is another.",
            text_type_text,
        )

        test = split_nodes_links([node])

        result = [
            TextNode("to boot", text_type_link, "https://www.boot.dev"),
            TextNode(" That was a link ", text_type_text),
            TextNode(
                "to youtube", text_type_link, "https://www.youtube.com/@bootdotdev"
            ),
            TextNode(" here is another.", text_type_text),
        ]
        self.assertEqual(test, result)

    ## Test split_node_links with no present links
    def test_split_node_no_links(self):
        node = TextNode(
            "That was a link here is another.",
            text_type_text,
        )

        test = split_nodes_links([node])

        result = [
            TextNode(
                "That was a link here is another.",
                text_type_text,
            )
        ]
        self.assertEqual(test, result)


if __name__ == "__main__":
    unittest.main()
