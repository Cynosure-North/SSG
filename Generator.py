import os
import tkinter.filedialog
import shutil
import markdown2

# Flags
dither_png = True


def walk(source_dir, target_dir):
    if os.path.exists(target_dir):
        if input(target_dir + " already exists, do you wish to continue. (y/n").lower() == 'n':
            exit()
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
            # Copy the files
            for file in files:
                # If they're markdown convert it
                if file.endswith(".md"):
                    content = markdown2.markdown(open(os.path.join(source_dir, root, file), "r").read())
                    with open(os.path.join(target_dir, root, os.path.splitext(file)[0] + ".html"), "w") as output:
                        for line in template:
                            output.write(line.replace("[Content]", content))

                else:
                    shutil.copyfile(os.path.join(source_dir, current_folder, file),
                                    os.path.join(target_dir, current_folder, file))


source = tkinter.filedialog.askdirectory(title="Choose source folder")
target = tkinter.filedialog.askdirectory(title="Choose target folder")
target = os.path.join(target, os.path.basename(source))

print(source)
print(target)

walk(source, target)
