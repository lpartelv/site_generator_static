import re
from inline_markdown import *
from htmlnode import *


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    result = []
    for block in blocks:
        if block == "":
            continue
        result.append(block.strip())
    return result

def block_to_block_type(block):
    if re.fullmatch(r"\#{1,6} .+", block):
        return "heading"
    if block.startswith("```") and block.endswith("```"):
        return "code"
    lines = block.split("\n")
    if len(re.findall(r">.*", block)) == len(lines):
        return "quote"
    if len(re.findall(r"^\* .*|\n\* .*", block)) == len(lines) or len(re.findall(r"^- .*|\n- .*", block)) == len(lines):
        return "unordered list"
    matches = re.findall(r"(\d)\. .*", block)
    if len(matches) != len(lines):
        return "paragraph"
    for i in range(len(matches)):
        if i + 1 != int(matches[i]):
            return "paragraph"
        if i + 1 == len(matches):
            return "ordered list"
    return "paragraph"
    
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return text_nodes_to_html_nodes(text_nodes)

def block_to_htmlnode(block):
    block_type = block_to_block_type(block)
    if block_type == "paragraph":
        return paragraph_to_htmlnode(block)
    if block_type == "heading":
        return heading_to_htmlnode(block)
    if block_type == "code":
        return code_to_htmlnode(block)
    if block_type == "quote":
        return quote_to_htmlnode(block)
    if block_type == "ordered list":
        return ordered_list_to_htmlnode(block)
    if block_type == "unordered list":
        return unordered_list_to_htmlnode(block)
    
def paragraph_to_htmlnode(block):
    text = block.split("\n")
    text = " ".join(text)
    children = text_to_children(text)
    return ParentNode("p", children)

def heading_to_htmlnode(block):
    last_star_index = block.find(" ")
    if last_star_index < 1 or last_star_index > 6:
        raise ValueError("Invalid heading level")
    tag = "h" + str(last_star_index)
    text = block[last_star_index + 1:]
    children = text_to_children(text)
    return ParentNode(tag, children)

def code_to_htmlnode(block):
    text = block[3:-3]
    children = text_to_children(text)
    return ParentNode("code", children)

def quote_to_htmlnode(block):
    lines = block.split("\n")
    lines = map(lambda x: x.lstrip(">").strip(), lines)
    text = " ".join(lines)
    children = text_to_children(text)
    return ParentNode("blockquote", children)

def ordered_list_to_htmlnode(block):
    list_items = []
    lines = block.split("\n")
    for line in lines:
        text = line.split(" ", 1)[1]
        children = text_to_children(text)
        list_items.append(ParentNode("li", children, None))
    return ParentNode("ol", list_items, None)

def unordered_list_to_htmlnode(block):
    list_items = []
    lines = block.split("\n")
    for line in lines:
        text = line.split(" ", 1)[1]
        children = text_to_children(text)
        list_items.append(ParentNode("li", children, None))
    return ParentNode("ul", list_items, None)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = block_to_htmlnode(block)
        children.append(html_node)
    return ParentNode("div", children, None)