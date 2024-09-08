import re
from htmlnode import ParentNode
from splitnode import text_to_textnodes
from textnode import text_node_to_html_node


## Convert a FULL markdown document into a single HTML node.
def markdown_to_html_node(markdown):
    final_list = []
    blocks = markdown_to_blocks(markdown)

    ## For each block, convert block into an html node and add into a list
    ## Returning a final ParentNode with block list added to children
    for block in blocks:
        if block == "":
            continue
        html_node = block_to_html_node(block)
        final_list.append(html_node)
    return ParentNode("div", final_list)


## Use predefined functions to apply modifications based on blocktype
def block_to_html_node(block):
    type = block_to_block_type(block)
    if type == "header":
        return block_to_header(block)
    if type == "quote":
        return block_to_quote(block)
    if type == "unordered list":
        return block_to_unordered_list(block)
    if type == "ordered list":
        return block_to_ordered_list(block)
    if type == "code":
        return block_to_code(block)
    if type == "paragraph":
        return block_to_paragraph(block)
    raise ValueError("Block type unknown")


## Take a string input and return a list of Inline Leaf Nodes
def text_to_children(text):
    node_list = text_to_textnodes(text)
    result = []
    for node in node_list:
        result.append(text_node_to_html_node(node))
    return result


## Convert a block to a header.
def block_to_header(text):
    split = text.split(" ", 1)
    tag = "h" + str(split[0].count("#"))
    text = text_to_children(split[1])
    return ParentNode(tag, text)


## Convert a block to a quote.
def block_to_quote(text):
    lines = text.split("\n")
    parsed = []

    for line in lines:
        if line == "":
            continue
        parsed.append(line.lstrip("> ").strip())
    result = " ".join(parsed)
    children = text_to_children(result)
    print(f"Text to children output:\n{children}")
    return ParentNode("blockquote", children)


## Convert a block to an unordered list.
def block_to_unordered_list(text):
    lines = text.split("\n")
    final_list = []

    for line in lines:
        if line == "":
            continue
        item = line[2:]
        children = text_to_children(item)
        final_list.append(ParentNode("li", children))
    return ParentNode("ul", final_list)


## Convert a block to an ordered list.
def block_to_ordered_list(text):
    lines = text.split("\n")
    line_items = []

    for line in lines:
        if line == "":
            continue
        item = line[3:]
        print(f"line item: {item}")
        children = text_to_children(item)
        line_items.append(ParentNode("li", children))

    return ParentNode("ol", line_items)


## Convert a block to code node
def block_to_code(text):
    lines = text[3:-3].strip()
    children = text_to_children(lines)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


## Convert a block to a paragraph node
def block_to_paragraph(text):
    lines = text.split("\n")
    result = " ".join(lines)
    children = text_to_children(result)
    print(f"Text to children output:\n{children}")
    return ParentNode("p", children)


## Take in a block of text and return its markdown type
def block_to_block_type(blocktype):
    type = "paragraph"

    ## If no input or nonetype then raise exception
    if blocktype is None or blocktype == " ":
        raise Exception("No input found!")

    ## HEADER
    if re.findall(r"^\#{1,6}\ *", blocktype):
        type = "header"

    ## CODE
    if re.findall(r"^\`{3}|.*`{3}$", blocktype):
        type = "code"

    ## QUOTE
    if re.findall(r"^\>\ ", blocktype, re.MULTILINE):
        lines = blocktype.splitlines()

        ## Iterate through each line and deterimine if line starts with ">"
        count = 0
        for line in lines:
            if re.findall(r"^\>\ ", line):
                count += 1

        print(f"count: {count} lines: {len(lines)}")
        if count == len(lines):
            type = "quote"

    ## UNORDERED LIST
    if re.findall(r"(^\*\ )|(^\-\ )", blocktype, re.MULTILINE):
        lines = blocktype.splitlines()

        line_count = len(lines) + 1

        if len(lines) == 1:
            return type

        count = 0
        for line in lines:
            if re.findall(r"(^\*\ )|(^\-\ )", line):
                count += 1

        if count == len(lines):
            type = "unordered list"

    ## ORDERED LIST
    if re.findall(r"^[1-9]\.\ ", blocktype):
        ## Split text into list of lines by \n.
        ## Take list and get a count of lines.
        split_text = blocktype.splitlines()

        ## Add + 1 to "line_count" to account for pythong starting at "0"
        line_count = len(split_text) + 1

        ## If list is one item or less, return as "paragraph"
        if line_count <= 2:
            return type

        count = 1
        for text in split_text:
            var = str(count) + ". "
            if re.findall((var + " *"), text):
                count += 1
            else:
                break

        if count == line_count:
            type = "ordered list"

    return type


## Take a markdown string as input and split into a list by separating
## with empty lines
def markdown_to_blocks(markdown):
    if markdown == "":
        raise Exception("No text found")

    final_list = []

    split_list = markdown.split("\n\n")

    for line in split_list:
        final_list.append(line)

    return final_list


def main():
    code = """```Here is some code
Here is some more code
Last bit of code```
"""


ordered_list = """1. This is a paragraph
2. Here is some **bold** text
3. Here is some *italic* text
"""

unordered_list = """- This is a paragraph
* Here is some **bold** text
- Here is some *italic* text
"""

quote = """>This is a text_quote\n> Here is another\n> and another"""
para = "Here is a *paragraph* of **text**"
header = "## This is a header"
quote = markdown_to_html_node(
    """>This is a text_quote\n> Here is another\n> and another"""
)
code = markdown_to_html_node("""```Here is some code\n and some more```""")

# end = markdown_to_html_node(quote)

text_quote = "> This is a quote\n> Here is another."

result = block_to_block_type(text_quote)

print(f"block type: {result}")


main()
