import os
import shutil

## Assign "root" variable and create paths for both "public" and "static"
root = os.getcwd().replace("/src", "")
public = os.path.join(root, "public")
static = os.path.join(root, "static")


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


def main():
    copy_static_to_public()


main()
