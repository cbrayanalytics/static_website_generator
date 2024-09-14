## Import required packages
import re
from textnode import TextNode

## Assign inline node type values to variables.
text_type_text = "text"
text_type_bold = "bold"
text_type_code = "code"
text_type_italic = "italic"
text_type_link = "link"
text_type_image = "image"


## Convert Text String to TextNodes(bold,italic,code,image,link)
def text_to_textnodes(text):
    if not text:
        raise Exception("No input found")

    node = [TextNode(text, text_type_text)]

    to_bold = split_nodes_delimiter(node, "**", text_type_bold)
    to_italic = split_nodes_delimiter(to_bold, "*", text_type_italic)
    to_code = split_nodes_delimiter(to_italic, "`", text_type_code)
    to_image = split_nodes_images(to_code)
    to_link = split_nodes_links(to_image)

    return to_link


## Extract bold,italic,code types from TextNode of "text" type.
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []

    for node in old_nodes:
        if node.text_type != text_type_text:
            new_list.append(node)
            continue
        else:
            split_text = node.text.split(delimiter)
            if len(split_text) % 2 == 0:
                raise Exception(f"invalid markdown syntax: {delimiter}")
            for i in range(len(split_text)):
                if split_text[i] == "":
                    continue
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

    for node in old_nodes:
        orig_text = node.text
        link_info = list(extract_markdown_links(orig_text))

        if link_info == []:
            new_list.extend([node])

        for link in link_info:
            link_alt = link[0]
            link_url = link[1]
            split_nodes = list(orig_text.split(f"[{link_alt}]({link_url})", 1))
            for item in split_nodes:
                if extract_markdown_links(item):
                    orig_text = item
                    continue
                if item == split_nodes[-1]:
                    if item != "":
                        new_list.extend([TextNode(item, text_type_text)])
                elif item != "":
                    new_list.extend([TextNode(item, text_type_text)])
                    new_list.extend([TextNode(link_alt, text_type_link, link_url)])
                else:
                    new_list.extend([TextNode(link_alt, text_type_link, link_url)])
    return new_list


## Extracts image "alt_text" and "image_link" from a given text input
def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


## Extracts link "alt_text" and "url_link" from a given text input
def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches
