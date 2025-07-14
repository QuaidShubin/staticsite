from textnode import TextNode, TextType
from inline_markdown import text_to_textnodes
import re


def main():

    text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    new_nodes = text_to_textnodes(text)
    for text_node in new_nodes:
        print("\n" + str(text_node) + "\n")


if __name__ == "__main__":
    main()
