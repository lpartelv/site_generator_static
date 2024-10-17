import re

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    result = []
    for block in blocks:
        if block == "":
            continue
        result.append(block.strip())
    return result

def block_to_block_type(block):
    if re.fullmatch(r"\*{1,6} .+", block):
        return "heading"
    if block.startswith("```") and block.endswith("```"):
        return "code"
    lines = block.split("\n")
    if len(re.findall(r">.*", block)) == len(lines):
        return "quote"
    if len(re.findall(r"^\* .*|\n\* .*", block)) == len(lines) or len(re.findall(r"^- .*|\n- .*", block)) == len(lines):
        return "unordered_list"
    matches = re.findall(r"(\d)\. .*", block)
    if len(matches) != len(lines):
        return "paragraph"
    for i in range(len(matches)):
        if i + 1 != int(matches[i]):
            return "paragraph"
        if i + 1 == len(matches):
            return "ordered_list"
    return "paragraph"

def markdown_to_html_node(markdown):

    return None