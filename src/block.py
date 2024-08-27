import re


## Take in a block of text and return its markdown type
def block_to_block_type(blocktype):
    type = "paragraph"

    if re.findall(r"^\#{1,6}\ *", blocktype):
        found = re.findall(r"^\#{1,6}\ *", blocktype)
        type = "Header"
        print(f"Header found: {found}")

    if re.findall(r"^\`{3}|.*`{3}$", blocktype):
        found = re.findall(r"^\`{3}.*\`{3}$", blocktype)
        type = "code"
        print(f"Code found: {found}")

    if re.findall(r"^\>", blocktype):
        found = re.findall(r"^\>", blocktype)
        type = "quote"
        print(f"Quote found: {found}")

        #    if re.findall(r"^(?=[(\*\-)\s])", blocktype, re.MULTILINE):
    if re.findall(r"(^\*\ )|(^\-\ )", blocktype, re.MULTILINE):
        lines = blocktype.splitlines()

        if len(lines) == 1:
            type = "paragraph"
            return type

        count = 0
        for line in lines:
            if re.findall(r"(^\*\ )|(^\-\ )", line):
                count += 1

        if count == len(lines):
            type = "unordered list"

    # if re.findall(r"^(![\d+\.\s+])", blocktype, re.MULTILINE):
    #     found = re.findall(r"^\*\ |^\-\ ", blocktype, re.MULTILINE)
    #     type = "unordered list"
    #     print(f"Unordered list found: {found}")

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


def main():
    header = " \n this is a line "

    print(f"header: {header}")
    block_to_block_type(header)


main()
