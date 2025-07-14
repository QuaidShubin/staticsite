import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    # def test_to_html(self):
    #     node = HTMLNode("div", "Hello, world!")
    #     self.assertEqual(node.to_html(), "<div>Hello, world!</div>")

    # def test_to_html_with_children(self):
    #     node = HTMLNode("div", "Hello, world!", [HTMLNode("p", "This is a paragraph")])
    #     self.assertEqual(
    #         node.to_html(), "<div>Hello, world!<p>This is a paragraph</p></div>"
    #     )

    # def test_to_html_with_props(self):
    #     node = HTMLNode("div", "Hello, world!", props={"class": "container"})
    #     self.assertEqual(node.to_html(), '<div class="container">Hello, world!</div>')

    def test_props_to_html_one_prop(self):
        node = HTMLNode("div", "Hello, world!", props={"class": "container"})
        self.assertEqual(node.props_to_html(), 'class="container"')

    def test_props_to_html_two_props(self):
        node = HTMLNode(
            "div", "Hello, world!", props={"class": "container", "id": "main"}
        )
        self.assertEqual(node.props_to_html(), 'class="container" id="main"')

    def test_props_to_html_no_props(self):
        node = HTMLNode("div", "Hello, world!")
        self.assertEqual(node.props_to_html(), "")


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


class TestParentNode(unittest.TestCase):
    def test_parent_to_html_div(self):
        node = ParentNode("div", [LeafNode("span", "child")])
        self.assertEqual(node.to_html(), "<div><span>child</span></div>")

    def test_parent_to_html_div_with_two_children(self):
        node = ParentNode(
            "div", [LeafNode("span", "child1"), LeafNode("span", "child2")]
        )
        self.assertEqual(
            node.to_html(), "<div><span>child1</span><span>child2</span></div>"
        )

    def test_parent_to_html_with_grandchildren(self):
        node = ParentNode("div", [ParentNode("span", [LeafNode("p", "child")])])
        self.assertEqual(node.to_html(), "<div><span><p>child</p></span></div>")

    def test_parent_to_html_no_children(self):
        node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_to_html_no_tag(self):
        node = ParentNode(None, [])
        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()
