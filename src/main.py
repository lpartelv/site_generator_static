from textnode import *
import os
import shutil
from block_markdown import markdown_to_html_node, extract_title
from htmlnode import *

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

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, encoding='utf-8') as src_file:
        src_data = src_file.read()
    with open(template_path, encoding='utf-8') as template_file:
        template_data = template_file.read()
    markdown_html = markdown_to_html_node(src_data).to_html()
    title = extract_title(src_data)
    template_data = template_data.replace("{{ Title }}", title).replace("{{ Content }}", markdown_html)
    if not os.path.exists(dest_path.split("/")[0]):
        os.mkdir(dest_path.split("/")[0])
    with open(dest_path, "a", encoding='utf-8') as dest_file:
        dest_file.write(template_data)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    entry_list = os.listdir(dir_path_content)
    for entry in entry_list:
        from_path = os.path.join(dir_path_content, entry)
        if os.path.isfile(from_path):
            to_path = os.path.join(dest_dir_path, entry.replace(".md", ".html"))
            generate_page(from_path, template_path, to_path)
        else:
            to_path = os.path.join(dest_dir_path, entry)
            os.mkdir(to_path)
            generate_pages_recursive(from_path, template_path, to_path)

def main():
    src = "./static"
    dst = "./public"
    if os.path.exists(dst):
        shutil.rmtree(dst)
    copy_paste_dir(src, dst)
    generate_pages_recursive("content/", "template.html", "public/")

main()