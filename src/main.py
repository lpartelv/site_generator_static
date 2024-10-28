from textnode import *
import os
import shutil

def copy_paste_dir(src, dst):
    if not os.path.exists(dst):
        os.mkdir(dst)
    src_list = os.listdir(src)
    for list_item in src_list:
        from_path = os.path.join(src, list_item)
        to_path = os.path.join(dst, list_item)
        if os.path.isfile(from_path):
            shutil.copy(from_path, to_path)
        else:
            copy_paste_dir(from_path, to_path)

def main():
    src = "./static"
    dst = "./public"
    if os.path.exists(dst):
        shutil.rmtree(dst)
    copy_paste_dir(src, dst)

main()