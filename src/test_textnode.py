import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)

        wrong_text_node = TextNode("This is another text node", TextType.BOLD)
        wrong_type_node = TextNode("This is a text node", TextType.TEXT)
        url_node = TextNode("This is a text node", TextType.BOLD, "www.google.com")

        self.assertNotEqual(node, wrong_text_node)
        self.assertNotEqual(node, wrong_type_node)
        self.assertNotEqual(node, url_node)

if __name__ == "__main__":
    unittest.main()
