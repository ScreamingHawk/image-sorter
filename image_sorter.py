import os
import shutil
import glob
import time
from PIL import Image

def create_dir(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)

def list_files(directory):
    files = []
    for ext in ('*.png', '*.jpg'):
        files.extend(glob.iglob(os.path.join(directory, "**", ext), recursive=True))
    return files

def copy_file_to(to_directory, filename):
    create_dir(to_directory)
    new_filename = os.path.join(to_directory, os.path.basename(filename))
    if not os.path.isfile(new_filename):
        shutil.copy2(os.path.join(filename), new_filename)

def copy_on_match(to_directory, filenames, match_size, exact_match=True, up_only=False, print_complete=True):
    start_time = time.time()
    copied = []
    for filename in filenames:
        with Image.open(filename, 'r') as img:
            if (not up_only or img.size[0] >= match_size[0]) and img.size[0]/img.size[1] == match_size[0]/match_size[1] and \
               (up_only or not exact_match or img.size[0] == match_size[0]):
                copy_file_to(to_directory, filename)
                copied.append(filename)
    if print_complete:
        print("Completed {} in {} seconds".format(to_directory, time.time()-start_time))
    return copied



from_directory = input("From directory: ")

filenames = list_files(from_directory)

print("Checking {} files".format(len(filenames)))

#1920x1080 and scales
copy_on_match('1920x1080', filenames, (1920, 1080), up_only=True)
#1080x1920 and scales
copy_on_match('phone', filenames, (1080, 1920), up_only=True)

