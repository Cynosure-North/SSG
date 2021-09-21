import os
import shutil
import click
import markdown2
from jinja2 import Environment, FileSystemLoader
import frontmatter


def walk(source_dir, target_dir, dither_png, copy_markdown, use_junctions):
    """
        Walk through every element in a source_dir and copy it to target_dir
        If it's a .md markdown file convert it to HTML
        If it's a .png file dither it TODO
    """

    if os.path.exists(target_dir):
        if input(target_dir + " already exists, do you wish to continue? This may overwrite some files (y/n) ").lower() == 'n':
            exit()
    else:
        os.mkdir(target_dir)

    for (root, dirs, files) in os.walk(source_dir):
        # Ignore hidden files
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']      # Assign in place so os.walk uses the updated array

        if root == source_dir:
            current_folder = ""
        else:
            current_folder = os.path.relpath(root, source_dir)

        # Copy the folder Structure
        if current_folder and not os.path.exists(os.path.join(target_dir, current_folder)):
            os.mkdir(os.path.join(target_dir, current_folder))

        if use_junctions and not root == source_dir \
                and not os.path.basename(root).startswith("-") and not os.path.basename(root).startswith("__"):

            out_file = make_junctions(source_dir, current_folder, dirs, files)
            with open(os.path.join(target_dir, current_folder, "__junction__.html"), "w") as output:
                output.write(out_file)

        for file in files:
            source_file = os.path.join(source_dir, current_folder, file)
            target_file = os.path.join(target_dir, current_folder, file)

            # Convert
            if file.endswith(".md"):
                if copy_markdown and not source_file == target_file:
                    shutil.copyfile(source_file, target_file)

                out_file = MD_to_HTML(source_file)
                with open(os.path.splitext(target_file)[0] + ".html", "w") as output:
                    output.write(out_file)
            # Dither
            elif file.endswith(".png") and dither_png:
                pass    # TODO
            # Copy                  This prevents SameFileError
            elif not source_file == target_file:
                shutil.copyfile(source_file, target_file)


def make_junctions(source_dir, root, dirs, files):  # TODO: Not working
    """
        Takes a folder, and all contents and returns the code for a __junction__ page
        This has links to all subfolders' __junction__ pages and all content in the folder
    """
    hierarchy = get_hierarchy(root)
    # Load in all the places to link to
    pages = [load_key_details(source_dir, root, y) for y in files
             if not y.startswith("-") and (y.endswith(".md") or y.endswith(".html"))]
    # Add the junction files for subfolders
    pages += [{"title": z, "description": "", "address": os.path.join(root, z, "__junction__.html")}
                          for z in dirs if not z.startswith("-")]       # TODO: It would be nice to prevent subfolders too
    template = env.get_template("junction.html")
    return template.render(hierarchy=hierarchy, pages=pages, title=os.path.basename(root))        # TODO: What


def get_hierarchy(root):        # TODO: it probably doesn't have a slash at the start which I need
    """
        Takes a folder and calculates every __junction__ file above it
    """

    hierarchy = []
    while root != os.path.split(root)[0]:
        # I'm not sure why, but this has to be append, rather than += or [len(hierarchy):]. Odd
        hierarchy.append({"title": os.path.split(root)[1], "address": os.path.join(root, "__junction__.html")})
        root = os.path.split(root)[0]
    return hierarchy


def load_key_details(source_dir, root, file):
    """
        Takes a filepath to a valid markdown file and returns:
        The title
        The description
        The address

        Or takes a filepath to a file and returns
        The title - The filename without the extension
        The description - [blank]
        The address

        Not especially necessary, but it saves an extra call to frontmatter.load
    """
    if file.endswith(".md"):
        page = frontmatter.load(os.path.join(source_dir, root, file))
        return {"title": page["title"], "description": page["description"],
                "address": os.path.join(root, os.path.splitext(file)[0] + ".html")}
    else:   # HTML file
        return {"title": os.path.splitext(file)[0],
                "description": "",
                "address": os.path.join(root, file)}


def MD_to_HTML(file):
    """
        Converts a filepath to a valid markdown file into HTML
        Make sure it's valid, and the template is in /__templates__
    """
    # Converts a markdown file to a valid
    post = frontmatter.load(file)
    template = env.get_template(post['template'] + ".html")
    return template.render(content=markdown2.markdown(post.content), title=post['title'],
                           description=post['description'], time=post['time'])


@click.command()
@click.option("-s", "--source", type=click.Path(exists=True), prompt=True, help="Where to get the files")
@click.option("-t", "--target", type=click.Path(exists=True, writable=True), prompt=True,
              help="Where to put the output (this doesn't make a folder)")
@click.option("-d/-D", "--dither/--no-Dither", default=True, help="Dither PNGs? (TODO)")
@click.option("-m/-M", "--markdown/--no-Markdown", default=False, help="Copy markdown files into output?")
@click.option("-j/-J", "--junction/--no-junction", default=True,
              help="Generate __junction__files linking to contents of each folder?")
def main(source, target, dither, markdown, junction):
    source = os.path.normpath(source)
    target = os.path.normpath(target)

    if not os.path.isfile(source):                                  # TODO: it doesn't work if prompted
        if not os.path.isdir(os.path.join(source, "__templates__")):
            print("__templates__ not found")
            exit()
        global env
        env = Environment(loader=FileSystemLoader(os.path.join(source, "__templates__")))

        walk(source, target, dither, markdown, junction)

    else:       # Pointed to a file
        out_file = MD_to_HTML(source)
        with open(target, "w") as output:
            output.write(out_file)


if __name__ == "__main__":
    main()
