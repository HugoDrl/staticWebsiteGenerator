from htmlnode import HTMLNode, HTMLParentNode
from process import text_node_to_html_node, text_to_text_nodes
from process_blocks import identify_block, separate_blocks
from textnode import BlockType, TextNode, TextType

def markdown_to_html_node(markdown: str) -> HTMLNode:
    html_nodes: list[HTMLNode] = []
    blocks = separate_blocks(markdown)

    for block in blocks:
        block_type = identify_block(block)

        if block_type != BlockType.CODE:
            text = sanitize_block(block)
            nodes = text_to_text_nodes(text)
            children=[text_node_to_html_node(node) for node in nodes]
            parent = HTMLParentNode(tag=block_type.value, children=children)
        else:
            text = block[4:-3]
            pre_node = HTMLParentNode(tag="code", children=[text_node_to_html_node(TextNode(text=text, text_type=TextType.TEXT))])
            parent = HTMLParentNode(tag="pre", children=[pre_node])

        html_nodes.append(parent)

    return HTMLParentNode(tag="div", children=html_nodes)

def sanitize_block(block: str) -> str:
    return block.replace("\n", " ")
