from htmlnode import LeafNode


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, node_two):
        if (
            self.text == node_two.text
            and self.text_type == node_two.text_type
            and self.url == node_two.url
        ):
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node):
    if text_node.text_type == "text":
        return LeafNode(None, text_node.text)
    if text_node.text_type == "bold":
        return LeafNode("b", text_node.text)
    if text_node.text_type == "italic":
        return LeafNode("i", text_node.text)
    if text_node.text_type == "code":
        return LeafNode("code", text_node.text)
    if text_node.text_type == "link":
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == "image":
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise Exception("Text Type Unknown")


def main():
    test = TextNode("This is a text node", "link", "https://www.boot.dev")
    testtwo = TextNode("This is a photo of a bug", "image", "/home/photos/butterfly")

    result = text_node_to_html_node(testtwo)

    print(f"Text Node to HTML result: {result.to_html()}")

    # print(f"Print results: {test.__repr__()}")
    # print(f"eg results: {test.__eq__(testtwo)}")


main()
