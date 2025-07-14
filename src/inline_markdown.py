from textnode import TextNode, TextType


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
