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


def main():
    test = TextNode("This is a text node", "bold", "https://www.boot.dev")
    testtwo = TextNode("This is a text node", "bold", "https://www.boot.dev")

    print(f"Print results: {test.__repr__()}")
    print(f"eg results: {test.__eq__(testtwo)}")


main()
