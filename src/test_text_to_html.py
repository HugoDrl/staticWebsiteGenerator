import unittest

from htmlnode import HTMLLeafNode, HTMLParentNode
from process import extract_markdown_images_or_links, split_nodes_delimiter, text_node_to_html_node, text_to_text_nodes
from process_blocks import identify_block
from process_html import extract_title, markdown_to_html_node
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

class TestTextToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """```
This is text that _should_ remain
the **same** even with inline stuff
```"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_list(self):
        md = """- buy milk
- convert this list
- take milk back"""
        expected = "<div><ul><li>buy milk</li><li>convert this list</li><li>take milk back</li></ul></div>"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, expected)

    def test_ordered_list(self):
        md = """1. get out
2. do stuff
3. get back in"""
        expected = "<div><ol><li>get out</li><li>do stuff</li><li>get back in</li></ol></div>"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, expected)

    def test_image_in_paragraph(self):
        md = "hey this is just a simple ![paragraph](https://paragraph) !"
        expected = '<div><p>hey this is just a simple <img src="https://paragraph" alt="paragraph"></img> !</p></div>'
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, expected)

    def test_multiple_blocks(self):
        md = """So i was like,


- Hey
- Hey

And that was it..
I don't know man."""
        expected = "<div><p>So i was like,</p><ul><li>Hey</li><li>Hey</li></ul><p>And that was it.. I don't know man.</p></div>"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, expected)

    def test_quote(self):
        md= """> Citation
> Citation2
> Source"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><blockquote>Citation\nCitation2\nSource</blockquote></div>"
        self.assertEqual(html, expected)

class TestExtractTitle(unittest.TestCase):

    def test_raise_h2(self):
        def func():
            text = "## title h2"
            return extract_title(text)
        self.assertRaises(Exception, func)

    def test_return_h1(self):
        title = extract_title("# TITLE")
        self.assertEqual(title, "TITLE")


if __name__ == "__main__":
    unittest.main()
