import unittest

from htmlnode import HTMLLeafNode
from main import text_node_to_html_node
from textnode import TextNode, TextType

class TestConvertTextToHTMLNode(unittest.TestCase):

    def test_convert_text(self):
        textnode = TextNode(text="hey", text_type=TextType.TEXT)
        htmlnode = HTMLLeafNode(tag=None, value="hey")
        self.assertEqual(text_node_to_html_node(textnode).to_html(), htmlnode.to_html())

    def test_convert_bold(self):
        textnode = TextNode(text="hey", text_type=TextType.BOLD)
        htmlnode = HTMLLeafNode(tag="b", value="hey")
        self.assertEqual(text_node_to_html_node(textnode).to_html(), htmlnode.to_html())

    def test_convert_italic(self):
        textnode = TextNode(text="hey", text_type=TextType.ITALIC)
        htmlnode = HTMLLeafNode(tag="i", value="hey")
        self.assertEqual(text_node_to_html_node(textnode).to_html(), htmlnode.to_html())

    def test_convert_code(self):
        textnode = TextNode(text="hey", text_type=TextType.CODE)
        htmlnode = HTMLLeafNode(tag="code", value="hey")
        self.assertEqual(text_node_to_html_node(textnode).to_html(), htmlnode.to_html())

    def test_convert_link(self):
        textnode = TextNode(text="hey", text_type=TextType.LINK, url="www.google.com")
        htmlnode = HTMLLeafNode(tag="a", value="hey", props={"href": "www.google.com"})
        self.assertEqual(text_node_to_html_node(textnode).to_html(), htmlnode.to_html())

    def test_convert_image(self):
        textnode = TextNode(text="hey", text_type=TextType.IMAGE, url="www.google.com")
        htmlnode = HTMLLeafNode(tag="img", value="", props={"src": "www.google.com", "alt": "hey"})
        self.assertEqual(text_node_to_html_node(textnode).to_html(), htmlnode.to_html())

if __name__ == "__main__":
    unittest.main()
