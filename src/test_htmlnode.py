import unittest

from htmlnode import HTMLNode, HTMLLeafNode

class TestHTMLNode(unittest.TestCase):

    def testeq(self):
        node = HTMLNode()
        expected = ""
        self.assertEqual(node.props_to_html(), expected)

        node2 = HTMLNode("a", "test", [node])
        expected2 = ""
        self.assertEqual(node2.props_to_html(), expected2)

        node3 = HTMLNode(props={"href": "www.google.com", "target": "google"})
        expected3 = " href=www.google.com target=google"
        self.assertEqual(node3.props_to_html(), expected3)

    def test_leaf_props(self):
        node = HTMLLeafNode("p", "test")
        expected = "<p>test</p>"
        self.assertEqual(node.to_html(), expected)
        
        node2 = HTMLLeafNode("a", "google", props={"href": "www.google.com"})
        expected2 = "<a href=www.google.com>google</a>"
        self.assertEqual(node2.to_html(), expected2)

if __name__ == "__main__":
    unittest.main()
