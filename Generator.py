import os
import click
import shutil
import markdown2

# Flags
dither_png = True


def walk(source_dir, target_dir):
    if os.path.exists(target_dir):
        if input(target_dir + " already exists, do you wish to continue. (y/n)").lower() == 'n':
            exit()
    else:
        os.mkdir(target_dir)

    with open("template.html", "r") as template:
        for (root, dirs, files) in os.walk(source_dir):
            # Ignore hidden files
            files = [f for f in files if not f[0] == '.']
            dirs[:] = [d for d in dirs if not d[0] == '.']

            # Copy the folder Structure
            current_folder = os.path.relpath(root, source_dir)
            if root != source_dir:
                os.mkdir(os.path.join(target_dir, current_folder))

            for file in files:
                # If they're markdown convert it
                if file.endswith(".md"):
                    content = markdown2.markdown(open(os.path.join(source_dir, root, file), "r").read())
                    with open(os.path.join(target_dir, root, os.path.splitext(file)[0] + ".html"), "w") as output:
                        for line in template:
                            output.write(line.replace("[Content]", content))
                # Copy the files
                else:
                    shutil.copyfile(os.path.join(source_dir, current_folder, file),
                                    os.path.join(target_dir, current_folder, file))


@click.command()
@click.option("-s", "--source", type=str, default=os.getcwd(), show_default=True)
@click.option("-t", "--target", type=str, default=os.getcwd(), show_default=True)
@click.option("-d/-D", "--dither/--no-Dither", default=True, show_default=True)
def main(source, target, dither):
    dither_png = dither
    walk(source, target)


if __name__ == "__main__":
    main()
