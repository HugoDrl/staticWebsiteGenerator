from htmlnode import HTMLLeafNode, HTMLNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    match text_node.text_type:
        case TextType.TEXT:
            return HTMLLeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return HTMLLeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return HTMLLeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return HTMLLeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return HTMLLeafNode(tag="a", value=text_node.text, props={"href": text_node.url or ""})
        case TextType.IMAGE:
            return HTMLLeafNode(tag="img", value="", props={"src": text_node.url or "", "alt": text_node.text})

def split_nodes_delimiter(nodes: list[TextNode], delimiter: str, new_type: TextType):
    new_nodes: list[TextNode] = []
    for node in nodes:
        splitted_nodes = node.text.split(delimiter)
        if len(splitted_nodes) == 1:
            new_nodes.append(node)
            continue
        if len(splitted_nodes) % 2 == 0:
            raise Exception("Not a valid markdown syntax")
        for index in range(len(splitted_nodes)):
            text = splitted_nodes[index]
            if not text:
                continue
            if index % 2 == 0:
                text_type = node.text_type
            else:
                text_type = new_type
            new_nodes.append(TextNode(text=text, text_type=text_type))
    return new_nodes
