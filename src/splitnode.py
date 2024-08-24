import re
from textnode import TextNode

text_type_text = "text"
text_type_bold = "bold"
text_type_code = "code"
text_type_italic = "italic"
text_type_link = "link"
text_type_image = "image"


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


## split text node into several text nodes, extracting images as a separate text node.
## Returns a list of text nodes
def split_nodes_images(old_nodes):
    new_list = []

    for node in old_nodes:
        orig_text = node.text
        image_info = list(extract_markdown_images(orig_text))

        if image_info == []:
            new_list.extend([node])

        for image in image_info:
            image_alt = image[0]
            image_link = image[1]
            split_nodes = list(orig_text.split(f"![{image_alt}]({image_link})", 1))
            for item in split_nodes:
                if extract_markdown_images(item):
                    orig_text = item
                    continue
                if item == split_nodes[-1]:
                    if item != "":
                        new_list.extend([TextNode(item, text_type_text)])
                elif item != "":
                    new_list.extend([TextNode(item, text_type_text)])
                    new_list.extend([TextNode(image_alt, text_type_image, image_link)])
                else:
                    new_list.extend([TextNode(image_alt, text_type_image, image_link)])
    return new_list


## split text node into several text nodes, extracting links as a separate text node
## Returns a list of text nodes
def split_nodes_links(old_nodes):
    new_list = []

    print(f"Starting nodes: {old_nodes}\n")

    for node in old_nodes:
        orig_text = node.text
        print(f"Text in node: {orig_text}\n")
        link_info = list(extract_markdown_links(orig_text))

        if link_info == []:
            new_list.extend([node])
            print(f"No link present: {node}")

        for link in link_info:
            print(f"current link: {link}\n")
            link_alt = link[0]
            link_url = link[1]
            split_nodes = list(orig_text.split(f"[{link_alt}]({link_url})", 1))
            print(f"split nodes: {split_nodes}\n")
            for item in split_nodes:
                if extract_markdown_links(item):
                    orig_text = item
                    continue
                if item == split_nodes[-1]:
                    if item != "":
                        new_list.extend([TextNode(item, text_type_text)])
                    else:
                        print("Empty last string!")
                elif item != "":
                    new_list.extend([TextNode(item, text_type_text)])
                    new_list.extend([TextNode(link_alt, text_type_link, link_url)])
                else:
                    new_list.extend([TextNode(link_alt, text_type_link, link_url)])

    print(f"Final list: {new_list}")

    return new_list


## Extracts image "alt_text" and "image_link" from a given text input
def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


## Extracts link "alt_text" and "url_link" from a given text input
def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches


def main():
    # node = TextNode("This is **text** node", text_type_code)
    # result = split_nodes_delimiter([node], "**", text_type_bold)
    # print(f"Result: {result}")

    # text = "This is a text with ![rowdy piper](https://example.org/first-time) and ![second roudn](https://example.org/second-time)"
    # print(extract_markdown_images(text))
    #
    # text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    # print(extract_markdown_links(text))

    print("TEST ONE!!")
    node = TextNode(
        "[to boot dev](https://www.boot.dev) This was a link [to youtube](https://www.youtube.com/@bootdotdev) here is another.",
        text_type_text,
    )

    new_nodes = split_nodes_links([node])
    print(f"split nodes links result: {new_nodes}")

    print("TEST TWO!!")
    node = TextNode(
        "This was a link [to boot dev](https://www.boot.dev) here is another [to youtube](https://www.youtube.com/@bootdotdev)",
        text_type_text,
    )

    new_nodes = split_nodes_links([node])
    print(f"split nodes links result: {new_nodes}")


main()
