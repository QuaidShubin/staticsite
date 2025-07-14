from textnode import TextNode, TextType
import re
from functools import partial


def text_to_textnodes(text):
    functions = [
        split_nodes_image,
        split_nodes_link,
        partial(split_nodes_inline_delimiter, delimiter="**", text_type=TextType.BOLD),
        partial(split_nodes_inline_delimiter, delimiter="_", text_type=TextType.ITALIC),
        partial(split_nodes_inline_delimiter, delimiter="`", text_type=TextType.CODE),
    ]
    curr_text_nodes = [TextNode(text, TextType.TEXT)]
    for func in functions:
        curr_text_nodes = func(curr_text_nodes)
    return curr_text_nodes


def split_nodes_inline_delimiter(old_nodes, delimiter, text_type):
    res = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            res.append(node)
            continue
        splitted_text = node.text.split(delimiter)
        if len(splitted_text) % 2 == 0:
            raise Exception("no closing delimiter found")

        for i, text in enumerate(splitted_text):
            if i % 2 == 0:
                curr_text_type = TextType.TEXT
            else:
                curr_text_type = text_type
            splitted_text[i] = TextNode(text, curr_text_type)

        res.extend(splitted_text)

    return res


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        original_text = node.text
        matches = extract_markdown_images(original_text)

        if not matches:
            new_nodes.append(node)
            continue

        curr_text = original_text
        for image_alt, image_link in matches:
            sections = curr_text.split(f"![{image_alt}]({image_link})", 1)
            leading_text = sections[0]
            if leading_text:
                new_nodes.append(TextNode(leading_text, TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            curr_text = sections[1]

        if curr_text:
            new_nodes.append(TextNode(curr_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        original_text = node.text
        matches = extract_markdown_links(original_text)

        if not matches:
            new_nodes.append(node)
            continue

        curr_text = original_text
        for link_alt, link_url in matches:
            sections = curr_text.split(f"[{link_alt}]({link_url})", 1)
            leading_text = sections[0]
            if leading_text:
                new_nodes.append(TextNode(leading_text, TextType.TEXT))
            new_nodes.append(TextNode(link_alt, TextType.LINK, link_url))
            curr_text = sections[1]

        if curr_text:
            new_nodes.append(TextNode(curr_text, TextType.TEXT))

    return new_nodes


# helper methods for images and links


def extract_markdown_images(text):

    pattern = r"!\[([^\]]*)\]\(([^)]*)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text):

    pattern = r"(?<!\!)\[([^\]]*)\]\(([^)]*)\)"
    return re.findall(pattern, text)
