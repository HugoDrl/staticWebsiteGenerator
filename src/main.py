from htmlnode import HTMLNode, HTMLLeafNode
from textnode import TextType, TextNode

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

def main():
   pass 
main()
