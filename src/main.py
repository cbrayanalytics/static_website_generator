## Import required modules
import os
import shutil
import re
from pathlib import Path
from block import markdown_to_html_node

## Assign "root" variable and create paths for both "public", "static", and "content"
root = os.getcwd().replace("/src", "")
public = os.path.join(root, "public")
static = os.path.join(root, "static")
content = os.path.join(root, "content")
template = os.path.join(root, "template.html")


## Copy files from "static" directory to "public" recursively
def copy_file(files, dir, loc):
    if len(files) > 0:
        file = os.path.join(dir, files[0])
        if not os.path.isdir(file):
            src = os.path.join(static, file)
            shutil.copy(src, loc)
            copy_file(files[1:], dir, loc)
        else:
            location = os.path.join(public, files[0])
            os.mkdir(location)
            path = os.path.join(static, files[0])
            content = os.listdir(path)
            copy_file(content, path, location)
            copy_file(files[1:], dir, loc)


## Check for existence of "public" directory and create if not
## If exists, remove current Contents
## Finally, run copy_file(from above)
def copy_static_to_public():
    contents = os.listdir(static)
    if os.path.exists(public):
        shutil.rmtree(public)
        os.mkdir(public)
        copy_file(contents, static, public)
    else:
        os.mkdir(public)
        copy_file(contents, static, public)


## Extract an H1 header from markdown document, format, then return.
def extract_title(markdown):
    title = re.search(r"^\#\ .*", markdown, re.MULTILINE)
    if title is None:
        raise Exception("No title found")
    else:
        title = title[0].strip("# ").strip()
    return title


## Generate a single page from the "from_path" by converting to html, applying the template
## and finally write to "dest_path"
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    src = Path(from_path).read_text()
    tp = Path(template_path).read_text()

    html = markdown_to_html_node(src).to_html()
    title = extract_title(src)
    tmp = tp.replace("{{ Title }}", title).replace("{{ Content }}", html)

    new_html = open(dest_path, "w")
    new_html.write(tmp)
    new_html.close


## Recursively generate html page from any md page within the /content new_folder
## of home directory within static website project
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if len(dir_path_content) > 0:
        curr_item = os.path.join(content, dir_path_content[0])
        if not os.path.isdir(curr_item):
            if ".md" in curr_item:
                index = dir_path_content[0].replace(".md", ".html")
                dp = os.path.join(dest_dir_path, index)
                generate_page(curr_item, template_path, dp)
            generate_pages_recursive(dir_path_content[1:], template_path, dest_dir_path)
        else:
            new_dir = os.listdir(curr_item)
            new_dir = list(
                map(lambda new_file: dir_path_content[0] + "/" + new_file, new_dir)
            )
            new_folder = os.path.join(dest_dir_path, dir_path_content[0]) + "/"

            if not os.path.exists(new_folder):
                os.mkdir(new_folder)

            generate_pages_recursive(new_dir, template_path, dest_dir_path)
            generate_pages_recursive(dir_path_content[1:], template_path, dest_dir_path)


def main():
    ## Remove current public directory contents and copy static contents to public directory
    ## Create public directory if does not exist.
    copy_static_to_public()
    #
    # Generate html page using from path with template path and place final copy in dest_path
    # generate_page("content/index.md", "template.html", "public/index.html")

    ## Create a listing of contents directory and apply to recursive function.
    listing = os.listdir(content)
    generate_pages_recursive(listing, template, public)


main()
