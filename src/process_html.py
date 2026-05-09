from re import findall
from htmlnode import HTMLNode, HTMLParentNode
from process import text_node_to_html_node, text_to_text_nodes
from process_blocks import identify_block, separate_blocks
from textnode import BlockType, TextNode, TextType

def markdown_to_html_node(markdown: str) -> HTMLNode:
    html_nodes: list[HTMLNode] = []
    blocks = separate_blocks(markdown)

    for block in blocks:
        block_type, tag = define_tag(block)

        match block_type:
            case BlockType.CODE:
                text = block[4:-3]
                pre_node = HTMLParentNode(tag="code", children=[text_node_to_html_node(TextNode(text=text, text_type=TextType.TEXT))])
                parent = HTMLParentNode(tag="pre", children=[pre_node])
            case BlockType.UNORDERED_LIST|BlockType.ORDERED_LIST:
                points = block.split("\n")
                nodes: list[TextNode] = []
                for point in points:
                    sanitized_text = " ".join(point.split(" ")[1:])
                    nodes += text_to_text_nodes(f"<li>{sanitized_text}</li>")
                children = [text_node_to_html_node(node) for node in nodes]
                parent = HTMLParentNode(tag=tag, children=children)
            case _:
                text = sanitize_block(block)
                nodes = text_to_text_nodes(text)
                children=[text_node_to_html_node(node) for node in nodes]
                parent = HTMLParentNode(tag=tag, children=children)

        html_nodes.append(parent)

    return HTMLParentNode(tag="div", children=html_nodes)

def sanitize_block(block: str) -> str:
    return block.replace("\n", " ")

def define_tag(block: str) -> tuple[BlockType, str]:
    block_type = identify_block(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return block_type, "p"
        case BlockType.HEADING:
            counter = 0
            while block[counter] == "#":
                counter += 1
            return block_type, f"h{counter}"
        case BlockType.UNORDERED_LIST:
            return block_type, "ul"
        case BlockType.ORDERED_LIST:
            return block_type, "ol"

    return block_type, block_type.value
