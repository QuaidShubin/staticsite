from textnode import TextNode, TextType

import re


def main():
    my_node = TextNode(
        "This is some anchor text", TextType.LINK, "https://www.boot.dev"
    )
    print(my_node)

    pattern = r"!\[([^\]]+)\]\(([^)]+)\)"
    print("hi")
    print("patterns: ", re.findall(pattern, "![alt]()"))


if __name__ == "__main__":
    main()
