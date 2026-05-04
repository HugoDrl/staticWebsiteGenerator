import unittest

from htmlnode import HTMLLeafNode
from process import split_nodes_delimiter, text_node_to_html_node
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

class TestConvertTextNodes(unittest.TestCase):

    def test_invalid_syntax(self):

        def function_call(text_node: TextNode):
            def function_def():
                return split_nodes_delimiter(nodes=[text_node], delimiter="**", new_type=TextType.BOLD)
            return function_def

        textnode = TextNode(text="this is definitely **not a valid md", text_type=TextType.TEXT)
        self.assertRaises(Exception, function_call(textnode))

    def test_convert_text_to_code(self):
        textnode = TextNode(text="just call `main()`", text_type=TextType.TEXT)
        expected = [TextNode(text="just call ", text_type=TextType.TEXT),
                    TextNode(text="main()", text_type=TextType.CODE)]
        self.assertEqual(split_nodes_delimiter([textnode], "`", TextType.CODE), expected)

    def test_convert_it_bo(self):
        textnode = TextNode(text="hey **bold content and _italic_** !", text_type=TextType.TEXT)
        converted_bold = split_nodes_delimiter(nodes=[textnode], delimiter="**", new_type=TextType.BOLD)
        converted_it = split_nodes_delimiter(nodes=converted_bold, delimiter="_", new_type=TextType.ITALIC)

        expected = [
                TextNode(text="hey ", text_type=TextType.TEXT),
                TextNode(text="bold content and ", text_type=TextType.BOLD),
                TextNode(text="italic", text_type=TextType.ITALIC),
                TextNode(text=" !", text_type=TextType.TEXT),
                ]
        self.assertEqual(converted_it, expected)

    def test_do_not_convert(self):
        textnode = TextNode(text="hey, _how_ are you ?", text_type=TextType.TEXT)
        expected = [TextNode(text="hey, _how_ are you ?", text_type=TextType.TEXT)]

        self.assertEqual(split_nodes_delimiter(nodes=[textnode], delimiter="'", new_type=TextType.ITALIC), expected)

if __name__ == "__main__":
    unittest.main()
