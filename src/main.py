from textnode import TextType, TextNode

def main():
    node = TextNode(
            text="this is some text",
            text_type=TextType.TEXT,
            )
    print(node)

main()
