from textnode import TextType, TextNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT.value:
            new_nodes.append(old_node)
            continue
        result = []
        node_sections = old_node.text.split(delimiter)
        if len(node_sections) % 2 == 0:
            raise ValueError("Invalid markdown syntax")
        for i in range(len(node_sections)):
            if node_sections[i] == "":
                continue
            if i % 2 == 0:
                result.append(TextNode(node_sections[i], TextType.TEXT))
            else:
                result.append(TextNode(node_sections[i], text_type))
        new_nodes.extend(result)
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\]\[]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches
