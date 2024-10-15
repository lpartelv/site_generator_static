from textnode import *

def main():
    jou = TextNode("This is a text node", TextType.HTML, "https://www.boot.dev")
    tsau = jou.__repr__()
    print(tsau)

main()