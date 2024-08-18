from textnode import TextNode

text_type_text = "text"
text_type_bold = "bold"
text_type_code = "code"
text_type_italic = "italic"


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []

    for node in old_nodes:
        # print(f"Old nodes: {node.text_type}")
        # print(f"Old nodes: {node.text}")
        if node.text_type != text_type_text:
            new_list.append(node)
            # print("Not a text node!!")
            # print(f"new_list so far: {new_list}")
        else:
            # print(f"text type: {text_type}")
            # print(f"delimiter: {delimiter}")
            split_text = node.text.split(delimiter)
            if len(split_text) <= 2:
                raise Exception(f"invalid markdown syntax: {delimiter}")
            for i in range(len(split_text)):
                if i % 2 != 0:
                    new_list.extend([TextNode(split_text[i], text_type)])
                else:
                    new_list.extend([TextNode(split_text[i], text_type_text)])

    return new_list


def main():
    node = TextNode("This is **text** node", text_type_code)
    result = split_nodes_delimiter([node], "**", text_type_bold)
    print(f"Result: {result}")


main()
