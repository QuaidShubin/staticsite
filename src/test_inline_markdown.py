import unittest

from inline_markdown import (
    split_nodes_inline_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    """
    TEST BASIC SPLIT FUNCTION
    """

    def test_basic_split(self):
        nodes = [TextNode("This is **bold** text", TextType.TEXT)]
        result = split_nodes_inline_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " text")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_no_delimiter(self):
        nodes = [TextNode("No delimiter here", TextType.TEXT)]
        result = split_nodes_inline_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "No delimiter here")
        self.assertEqual(result[0].text_type, TextType.TEXT)

    def test_multiple_delimiters(self):
        nodes = [TextNode("**Bold** and **again**", TextType.TEXT)]
        result = split_nodes_inline_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, "")
        self.assertEqual(result[1].text, "Bold")
        self.assertEqual(result[2].text, " and ")
        self.assertEqual(result[3].text, "again")
        self.assertEqual(result[4].text, "")

    def test_unclosed_delimiter_raises(self):
        nodes = [TextNode("*Unclosed delimiter", TextType.TEXT)]
        with self.assertRaises(Exception):
            split_nodes_inline_delimiter(nodes, "*", TextType.BOLD)

    def test_italics_split(self):
        nodes = [TextNode("This is _italic_ text", TextType.TEXT)]
        result = split_nodes_inline_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "italic")
        self.assertEqual(result[1].text_type, TextType.ITALIC)
        self.assertEqual(result[2].text, " text")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_code_split(self):
        nodes = [TextNode("This is `code` text", TextType.TEXT)]
        result = split_nodes_inline_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "code")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[2].text, " text")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    """
    TEST IMAGE AND LINK MARKDOWN
    """

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_at_beginning(self):
        node = TextNode(
            "![start](url1) and then some text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("start", TextType.IMAGE, "url1"),
                TextNode(" and then some text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_right_after_each_other(self):
        node = TextNode(
            "![one](url1)![two](url2) after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("one", TextType.IMAGE, "url1"),
                TextNode("two", TextType.IMAGE, "url2"),
                TextNode(" after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_almost_but_not_quite(self):
        node = TextNode(
            "This is ![notanimage][url1] and ![alsonot](url2",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode(
                    "This is ![notanimage][url1] and ![alsonot](url2", TextType.TEXT
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com) and another [second link](https://www.test.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://www.test.com"),
            ],
            new_nodes,
        )

    def test_split_links_at_beginning(self):
        node = TextNode(
            "[start](url1) and then some text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("start", TextType.LINK, "url1"),
                TextNode(" and then some text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_right_after_each_other(self):
        node = TextNode(
            "[one](url1)[two](url2) after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("one", TextType.LINK, "url1"),
                TextNode("two", TextType.LINK, "url2"),
                TextNode(" after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_almost_but_not_quite(self):
        node = TextNode(
            "This is [notalink][url1] and [alsonot](url2",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is [notalink][url1] and [alsonot](url2", TextType.TEXT),
            ],
            new_nodes,
        )

    """
    TEST EXTRACTION
    """

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.example.com)"
        )
        self.assertListEqual([("link", "https://www.example.com")], matches)

    def test_extract_multiple_images(self):
        matches = extract_markdown_images("![one](url1) and ![two](url2)")
        self.assertListEqual([("one", "url1"), ("two", "url2")], matches)

    def test_extract_multiple_links(self):
        matches = extract_markdown_links("[first](url1) and [second](url2)")
        self.assertListEqual([("first", "url1"), ("second", "url2")], matches)

    def test_image_and_link_together(self):
        text = "![img](imgurl) and [link](linkurl)"
        img_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
        self.assertListEqual([("img", "imgurl")], img_matches)
        self.assertListEqual([("link", "linkurl")], link_matches)

    def test_image_with_missing_url(self):
        matches = extract_markdown_images("![alt]()")
        self.assertListEqual([("alt", "")], matches)

    def test_link_with_missing_url(self):
        matches = extract_markdown_links("[text]()")
        self.assertListEqual([("text", "")], matches)

    def test_invalid_image_syntax(self):
        matches = extract_markdown_images("![alt][url]")
        self.assertListEqual([], matches)

    def test_invalid_link_syntax(self):
        matches = extract_markdown_links("[text][url]")
        self.assertListEqual([], matches)

    def test_escaped_image_not_matched_by_link(self):
        text = "This is ![notalink](url) and [alink](url)"
        link_matches = extract_markdown_links(text)
        self.assertListEqual([("alink", "url")], link_matches)

    """
    TEST FINAL FUCNTION
    """

    def test_text_to_textnodes_base_1(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )
