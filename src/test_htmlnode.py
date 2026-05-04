import unittest

from htmlnode import HTMLNode, HTMLLeafNode, HTMLParentNode

class TestHTMLNode(unittest.TestCase):

    def testeq(self):
        node = HTMLNode()
        expected = ""
        self.assertEqual(node.props_to_html(), expected)

        node2 = HTMLNode("a", "test", [node])
        expected2 = ""
        self.assertEqual(node2.props_to_html(), expected2)

        node3 = HTMLNode(props={"href": "www.google.com", "target": "google"})
        expected3 = ' href="www.google.com" target="google"'
        self.assertEqual(node3.props_to_html(), expected3)

    def test_leaf_props(self):
        node = HTMLLeafNode("p", "test")
        expected = "<p>test</p>"
        self.assertEqual(node.to_html(), expected)

        node2 = HTMLLeafNode("a", "google", props={"href": "www.google.com"})
        expected2 = '<a href="www.google.com">google</a>'
        self.assertEqual(node2.to_html(), expected2)

class TestHTMLParentNode(unittest.TestCase):

    def test_empty_parent(self):
        node = HTMLParentNode(tag="p", children=[])
        self.assertRaises(ValueError, node.to_html)

    def test_parent(self):
        child1 = HTMLLeafNode(tag="p", value="hello")
        child2 = HTMLLeafNode(tag="a", value="click", props={"href": "http://unsecurelink"})
        parent = HTMLParentNode(tag="div", children=[child1, child2])

        expected = '<div><p>hello</p><a href="http://unsecurelink">click</a></div>'
        self.assertEqual(parent.to_html(), expected)

    def test_grandparent(self):
        child1 = HTMLLeafNode(tag="p", value="hello")
        child2 = HTMLLeafNode(tag="a", value="click", props={"href": "http://unsecurelink"})
        parent = HTMLParentNode(tag="div", children=[child1])
        grand_parent = HTMLParentNode(tag="div", children=[parent, child2], props={"class": "grand-parent"})

        expected = '<div class="grand-parent"><div><p>hello</p></div><a href="http://unsecurelink">click</a></div>'
        self.assertEqual(grand_parent.to_html(), expected)


if __name__ == "__main__":
    unittest.main()
