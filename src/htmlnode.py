
class HTMLNode:
    def __init__(self, tag: str|None = None, value: str|None = None, children: list["HTMLNode"]|None = None, props: dict[str, str]|None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        return_string: str = ""
        if not self.props:
            return ""
        for key, value in self.props.items():
            return_string += f" {key}={value}"

        return return_string

    def __repr__(self) -> str:
        return f"HTMLNode(tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props})"

class HTMLLeafNode(HTMLNode):
    def __init__(self, tag: str|None, value: str, props: dict[str, str]|None = None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError

        if not self.tag:
            return self.value

        entry_tag = "<" + self.tag
        entry_tag = entry_tag + super().props_to_html() + ">"

        return f"{entry_tag}{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"HTMLNode(tag: {self.tag}, value: {self.value}, props: {self.props})"

class HTMLParentNode(HTMLNode):
    def __init__(self, tag: str|None, children: list[HTMLNode], props: dict[str, str]|None = None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        pass
