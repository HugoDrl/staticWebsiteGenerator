from htmlnode import HTMLNode, HTMLParentNode
from process import text_node_to_html_node, text_to_text_nodes
from process_blocks import identify_block, separate_blocks
from textnode import BlockType, TextNode, TextType

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
        case BlockType.QUOTE:
            return block_type, "blockquote"

    return block_type, block_type.value

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
                text = sanitize_list(block)
                nodes: list[TextNode] = []
                for line in text:
                    nodes += text_to_text_nodes(line)

                children = [text_node_to_html_node(node) for node in nodes]
                parent = HTMLParentNode(tag=tag, children=children)

            case _:
                text = sanitize_block(block, block_type)
                nodes = text_to_text_nodes(text)
                children=[text_node_to_html_node(node) for node in nodes]
                parent = HTMLParentNode(tag=tag, children=children)

        html_nodes.append(parent)

    return HTMLParentNode(tag="div", children=html_nodes)

def sanitize_paragraph(block: str) -> str:
        return block.replace("\n", " ")

def sanitize_list(list: str) -> list[str]:

    lines = list.split("\n")
    return_lines: list[str] = []
    for line in lines:
        line = " ".join(line.split(" ")[1:])
        line = f"<li>{line}</li>"
        return_lines.append(line)
    return return_lines

def sanitize_quote(quote: str) -> str:
    lines = quote.split("\n")
    return_lines: list[str] = []
    for line in lines:
        if line.startswith("> "):
            line = line[2:]
        else:
            line = line[1:]
        return_lines.append(f'{line}')
    return f"{"\n".join(return_lines)}"

def sanitize_heading(heading: str) -> str:
    counter = 0
    while heading[counter] == "#" and counter < 6:
        counter+=1
    counter += 1
    return heading[counter:]

def sanitize_block(block: str, block_type: BlockType) -> str:
    match block_type:
        case BlockType.HEADING:
            return sanitize_heading(block)
        case BlockType.PARAGRAPH:
            return sanitize_paragraph(block)
        case BlockType.QUOTE:
            return sanitize_quote(block)
        case _:
            return block

def extract_title(md: str) -> str:
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise Exception("No title found !")
