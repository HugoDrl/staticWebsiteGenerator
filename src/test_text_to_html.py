import unittest

from htmlnode import HTMLLeafNode
from process import extract_markdown_images_or_links, split_nodes_delimiter, text_node_to_html_node
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

    def test_extract_image(self):
        text = "![description](link_image)"
        expected = [("description", "link_image")]
        self.assertEqual(extract_markdown_images_or_links(text, TextType.IMAGE), expected)

    def test_extract_images(self):
        text = "![description](link_image) and also ![test](test_image)"
        expected = [("description", "link_image"), ("test", "test_image")]
        self.assertEqual(extract_markdown_images_or_links(text, TextType.IMAGE), expected)

    def test_extract_links(self):
        text = "[description](link)"
        expected = [("description", "link")]
        self.assertEqual(extract_markdown_images_or_links(text, TextType.LINK), expected)

    def test_extract_wrong_type(self):
        text = "![description](link_image)"
        expected = []
        self.assertEqual(extract_markdown_images_or_links(text, TextType.LINK), expected)

    def test_extract_image_from_nodes(self):
        node = TextNode(text='hey look at my ![car](https://car) !', text_type=TextType.TEXT)
        expected = [
                TextNode(text="hey look at my ", text_type=TextType.TEXT),
                TextNode(text="car", text_type=TextType.IMAGE, url="https://car"),
                TextNode(text=" !", text_type=TextType.TEXT),
                ]
        self.assertEqual(
                split_nodes_delimiter([node], new_type=TextType.IMAGE, delimiter=""),
                expected
                )

    def test_only_link_from_nodes(self):
        node = TextNode(text='[car](https://car)', text_type=TextType.TEXT)
        expected = [
                TextNode(text="car", text_type=TextType.LINK, url="https://car"),
                ]
        self.assertEqual(
                split_nodes_delimiter([node], new_type=TextType.LINK, delimiter=""),
                expected
                )

    def test_extract_no_image_from_nodes(self):
        node = TextNode(text='hey look at my [car](https://car) !', text_type=TextType.TEXT)
        expected = [
                TextNode(text='hey look at my [car](https://car) !', text_type=TextType.TEXT)
                ]
        self.assertEqual(
                split_nodes_delimiter([node], new_type=TextType.IMAGE, delimiter=""),
                expected
                )

    def test_extract_image_and_link_from_nodes(self):
        node = TextNode(text='hey look at my ![car](https://car) and my new [house](https://house)', text_type=TextType.TEXT)
        expected = [
                TextNode(text="hey look at my ", text_type=TextType.TEXT),
                TextNode(text="car", text_type=TextType.IMAGE, url="https://car"),
                TextNode(text=" and my new ", text_type=TextType.TEXT),
                TextNode(text="house", text_type=TextType.LINK, url="https://house"),
                ]

        first = split_nodes_delimiter([node], new_type=TextType.IMAGE, delimiter="")
        second = split_nodes_delimiter(first, new_type=TextType.LINK, delimiter="")
        self.assertEqual(second, expected)

if __name__ == "__main__":
    unittest.main()
