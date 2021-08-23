import os
import tkinter.filedialog
import shutil
#import dither

#import dither
#import MD_to_HTML

#Flags
dither_png = True


source_dir = tkinter.filedialog.askdirectory(title="Choose source folder")
target_dir = tkinter.filedialog.askdirectory(title="Choose target folder")
target_dir = os.path.join(target_dir, os.path.basename(source_dir))

print(source_dir)
print(target_dir)


def walk(source_dir, target_dir):
    if os.path.exists(target_dir):
        pass
        #Todo Remove
    os.mkdir(target_dir)
    for (root, dirs, files) in os.walk(source_dir):
        #Ignore hidden files
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']

        #Copy the folder Structure
        current_folder = os.path.relpath(root, source_dir)
        if root != source_dir:
            os.mkdir(os.path.join(target_dir, current_folder))
        #Copy the files can convert if needed
        for file in files:
            if file.endswith(".md"):
                MD_to_HTML.convert(file)
            else:
                shutil.copyfile(os.path.join(source_dir, current_folder, file), os.path.join(target_dir, current_folder, file))
                
    ''' #TODO: Dither
            elif file.endswith(".png") and dither_png:
                pass
                #dither.dither(file
    '''

def copy(file):
    pass


walk(source_dir, target_dir)
