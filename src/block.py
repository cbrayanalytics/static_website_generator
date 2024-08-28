import re


## Take in a block of text and return its markdown type
def block_to_block_type(blocktype):
    type = "paragraph"

    ## If no input or nonetype then raise exception
    if blocktype is None or blocktype == " ":
        raise Exception("No input found!")

    ## HEADER
    if re.findall(r"^\#{1,6}\ *", blocktype):
        found = re.findall(r"^\#{1,6}\ *", blocktype)
        type = "Header"

    ## CODE
    if re.findall(r"^\`{3}|.*`{3}$", blocktype):
        found = re.findall(r"^\`{3}.*\`{3}$", blocktype)
        type = "code"

    ## QUOTE
    if re.findall(r"^\>", blocktype):
        lines = blocktype.splitlines()

        ## if only one line, then return "paragraph"
        if len(lines) == 1:
            return type

        ## Iterate through each line and deterimine if line starts with ">"
        count = 0
        for line in lines:
            if re.findall(r"^\>", line):
                count += 1

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

    split_list = markdown.strip().split("\n\n")

    for line in split_list:
        if line == "\n":
            continue
        if line == "":
            continue
        else:
            line = line.strip()
            final_list.append(line)

    print(f"Final list: {final_list}")

    return final_list
