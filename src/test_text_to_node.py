import unittest

from textnode import TextNode, TextType
from process import extract_markdown_images_or_links, split_nodes_delimiter, text_to_text_nodes
from process_blocks import separate_blocks

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

    def test_convert_multiples(self):
        textnode = TextNode(text="hey **bold** regular and **bold**", text_type=TextType.TEXT)
        converted_bold = split_nodes_delimiter(nodes=[textnode], delimiter="**", new_type=TextType.BOLD)

        expected = [
                TextNode(text="hey ", text_type=TextType.TEXT),
                TextNode(text="bold", text_type=TextType.BOLD),
                TextNode(text=" regular and ", text_type=TextType.TEXT),
                TextNode(text="bold", text_type=TextType.BOLD),
                ]
        self.assertEqual(converted_bold, expected)

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

    def test_extract_images_from_nodes(self):
        node = TextNode(text='hey look at my ![car](https://car) and my ![house](https://house)!', text_type=TextType.TEXT)
        expected = [
                TextNode(text="hey look at my ", text_type=TextType.TEXT),
                TextNode(text="car", text_type=TextType.IMAGE, url="https://car"),
                TextNode(text=" and my ", text_type=TextType.TEXT),
                TextNode(text="house", text_type=TextType.IMAGE, url="https://house"),
                TextNode(text="!", text_type=TextType.TEXT),
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

    def test_full_conversion(self):
        text = """Once uppon a time, a **troll** went to a _village_"""
        expected = [
                TextNode(text="Once uppon a time, a ", text_type=TextType.TEXT),
                TextNode(text="troll", text_type=TextType.BOLD),
                TextNode(text=" went to a ", text_type=TextType.TEXT),
                TextNode(text="village", text_type=TextType.ITALIC),
                ]

        self.assertEqual(text_to_text_nodes(text), expected)

    def test_code_images(self):
        text = "To code, you simply have to do `a = 1` and let the computer do the rest.![awesome](https://awesome)[please follow my tutorial](https://tutorial)"
        expected = [
                TextNode(text="To code, you simply have to do ", text_type=TextType.TEXT),
                TextNode(text="a = 1", text_type=TextType.CODE),
                TextNode(text=" and let the computer do the rest.", text_type=TextType.TEXT),
                TextNode(text="awesome", text_type=TextType.IMAGE, url="https://awesome"),
                TextNode(text="please follow my tutorial", text_type=TextType.LINK, url="https://tutorial"),
                ]

        self.assertEqual(text_to_text_nodes(text), expected)

class TestConvertTextBlock(unittest.TestCase):

    def test_split_blocks(self):
        text = """
        # This is a title

        This is a paragraph
        """
        expected = [
                "# This is a title",
                "This is a paragraph",
                ]

        self.assertEqual(separate_blocks(text), expected)

    def test_split_blocks_empty(self):
        text = """
        # This is a title


        This is a paragraph   
        """
        expected = [
                "# This is a title",
                "This is a paragraph",
                ]

        self.assertEqual(separate_blocks(text), expected)

if __name__ == "__main__":
    unittest.main()
