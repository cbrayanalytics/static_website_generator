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
    text = """ # This is a heading

     This is a paragraph of text. It has some **bold** and *italic* words inside of it.






     * This is the first list item in a list block
     * This is a list item
     * This is another list item  """

    markdown_to_blocks(text)


main()
