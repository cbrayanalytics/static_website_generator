import re


def block_to_block_type(blocktype):
    block = "paragraph"

    if blocktype is None or blocktype == "":
        raise Exception("No input found!")

    if re.findall(r"^[1-9]\.\ ", blocktype):
        ## Split text into list of lines by \n.
        ## Take list and get a count of lines.
        split_text = blocktype.splitlines()

        ## Add + 1 to "line_count" to account for pythong starting at "0"
        line_count = len(split_text) + 1
        print(f"line count: {line_count}")

        ## If list is one item or less, return as "paragraph"
        if line_count >= 2:
            print("not enough lines")
            return block

        count = 1
        for text in split_text:
            var = str(count) + ". "
            if re.findall((var + " *"), text):
                count += 1
            else:
                break

        if count == line_count:
            print("setting block to 'ordered list'")
            block = "ordered list"

    return block


def main():
    pass


main()
