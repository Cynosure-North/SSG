import os
import shutil
import click
import markdown2
from jinja2 import Environment, FileSystemLoader
import frontmatter


def walk(source_dir, target_dir):
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

        for file in files:
            if file.endswith(".md"):
                if copy_markdown and not os.path.join(source_dir, current_folder, file) == os.path.join(target_dir, current_folder, file):
                    shutil.copyfile(os.path.join(source_dir, current_folder, file),
                                    os.path.join(target_dir, current_folder, file))

                out_file = MD_to_HTML(os.path.join(source_dir, current_folder, file))
                with open(os.path.join(target_dir, current_folder, os.path.splitext(file)[0] + ".html"), "w") as output:
                    output.write(out_file)
            elif file.endswith(".png") and dither_png:
                pass    # TODO
            elif not os.path.join(source_dir, current_folder, file) == os.path.join(target_dir, current_folder, file):  # Prevents SameFileError
                shutil.copyfile(os.path.join(source_dir, current_folder, file),
                                os.path.join(target_dir, current_folder, file))


def MD_to_HTML(file):
    post = frontmatter.load(file)
    template = env.get_template(post['template'] + ".html")
    return template.render(content=markdown2.markdown(post.content), title=post['title'],
                           description=post['description'], time=post['time'])


@click.command()
@click.option("-s", "--source", type=str, default=os.getcwd(), show_default=True, help="Where to get the files")
@click.option("-t", "--target", type=str, default=os.getcwd(), show_default=True, help="Where to put the output (doesn't make a folder")
@click.option("-d/-D", "--dither/--no-Dither", default=True, show_default=True, help="Dither PNGs?")
@click.option("-m/-M", "--markdown/--no-Markdown", default=True, show_default=True, help="Copy markdown files into output?")
def main(source, target, dither, markdown):
    global dither_png
    dither_png = dither

    global copy_markdown
    copy_markdown = markdown

    global env
    env = Environment(loader=FileSystemLoader(os.path.join(source, "__templates__")))

    walk(source, target)


if __name__ == "__main__":
    main()
