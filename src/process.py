from re import findall

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

def split_nodes_delimiter(nodes: list[TextNode], delimiter: str, new_type: TextType) -> list[TextNode]:
    if new_type == TextType.IMAGE or new_type == TextType.LINK:
        return split_nodes_images_or_link(nodes, new_type)

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

def split_nodes_images_or_link(nodes: list[TextNode], type: TextType) -> list[TextNode]:
    match type:
        case TextType.IMAGE|TextType.LINK:
            pass
        case _:
            raise Exception("Only image or links can be extracted here")

    new_nodes: list[TextNode] = []
    for node in nodes:
        nodes = extract_node_images_or_links(node, type)
        new_nodes += nodes

    return new_nodes

def extract_node_images_or_links(node: TextNode, type: TextType) -> list[TextNode]:
    if type == TextType.IMAGE:
        starting_char = "!"
    else:
        starting_char = ""
    found_values = extract_markdown_images_or_links(node.text, type)
    if not found_values:
        return [node]

    current = [node]
    for value in found_values:
        sep = f"{starting_char}[{value[0]}]({value[1]})"
        next_current: list[TextNode] = []
        for n in current:
            splitted = n.text.split(sep)
            for i in range(len(splitted)):
                #Ignore if text is empty
                if splitted[i]:
                    next_current.append(TextNode(text=splitted[i], text_type=n.text_type, url=n.url))
                #Add new node (image or link) between each separated nodes, only if it is not the last one
                #This allows also to not add the new node if len(splitted) == 1, so it has not been found
                if i < len(splitted) - 1:
                    next_current.append(TextNode(text=value[0], text_type=type, url=value[1]))
        current = next_current

    return current

def extract_markdown_images_or_links(text: str, type: TextType) -> list[tuple[str, str]]:
    match type:
        case TextType.IMAGE:
            starting_char = r"\!"
        case TextType.LINK:
            starting_char = r"(?<!\!)"
        case _:
            raise Exception("Only images and links can be treated here")

    founds: list[tuple[str, str]] = findall(starting_char + r"\[(.*?)\]\((.*?)\)", text)
    return founds
