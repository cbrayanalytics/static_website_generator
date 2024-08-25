class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""
        string = ""
        for key, value in self.props.items():
            string = string + f' {key}="{value}"'
        return string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, props)
        self.tag = tag
        self.value = value
        self.props = props

    def to_html(self):
        string = ""
        if self.value is None:
            raise ValueError("all leaf nodes must have a value")
        if self.tag is None:
            return self.value
        if self.props is not None:
            for value in self.props:
                string = string + f' {value}="{self.props[value]}"'
            string = f"<{self.tag}" + string + f">{self.value}</{self.tag}>"
            return string
        string = f"<{self.tag}>{self.value}</{self.tag}>"
        return string


class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, children)
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self):
        if self.tag is None:
            raise ValueError("all parent nodes must have a tag")
        if self.children is None:
            raise ValueError("all parent nodes must have a children")

        # string = ""
        # for child in self.children:
        #     print(f"Child: {child}")
        #     result = child.to_html()
        #     print(f"Formatted child: {result}")
        #     string = string + result

        def child_to_string(result, child):
            if len(child) == 0:
                return result
            result = result + child[0].to_html()
            return child_to_string(result, child[1:])

        result = ""
        result = child_to_string(result, self.children)

        string = f"<{self.tag}>" + result + f"</{self.tag}>"
        return string


def main():
    node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
            ParentNode(
                "d",
                [
                    LeafNode("b", "nested bold text"),
                    LeafNode("i", "nested italic text"),
                ],
            ),
        ],
    )

    result = node.to_html()

    print(f"ParentNode to_html output: {result}")

    # node = HTMLNode(
    #     "a",
    #     "Hello there!",
    #     "children",
    #     {"href": "http://example.com", "target": "_blank"},
    # )
    #
    # result = node.props_to_html()
    #
    # print(f"repr output: {result}")


main()
