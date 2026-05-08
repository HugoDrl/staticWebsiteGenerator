from textnode import BlockType
from re import findall

def separate_blocks(text: str) -> list[str]:
    blocks = text.split("\n\n")
    valid_blocks: list[str] = []
    for block in blocks:
        block = block.strip()
        if block:
            valid_blocks.append(block)

    return valid_blocks

def identify_block(block: str) -> BlockType:
    title = findall(r"\#{1,6} ", block[:8])
    if title:
        return BlockType.HEADING

    if block[:4] == '```\n' and block[-3:] == '```':
        return BlockType.CODE

    lines = block.split("\n")
    for line in lines:
        if line and line[0] != ">":
            break
    else:
        return BlockType.QUOTE
    for line in lines:
        if len(line) >= 2 and line[:2] != "- ":
            break
    else:
        return BlockType.UNORDERED_LIST

    for i in range(1, len(lines)+1):
        if len(lines[i-1]) >= 3 and lines[i-1][:3] != f"{i}. ":
            break
    else:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
