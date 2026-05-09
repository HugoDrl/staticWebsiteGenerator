import os

from process_html import markdown_to_html_node

def delete_files(folder: str) -> None:
    for element in os.listdir(folder):
        if os.path.isdir(f"{folder}/{element}"):
            delete_files(f"{folder}/{element}")
            continue
        os.remove(f"{folder}/{element}")
    os.rmdir(folder)

def process_file(file: str, source_folder: str, destination_folder: str):
    if file.endswith(".md"):
        filename = file.replace(".md", ".html")
        with open(f"{source_folder}/{file}") as f:
            content = f.read()
        node = markdown_to_html_node(content)
        html = node.to_html()
        with open(f"{destination_folder}/{filename}", mode="w+") as w:
            w.write(html)
    else:
        with open(f"{source_folder}/{file}", mode="rb") as f:
            content = f.read()
        with open(f"{destination_folder}/{file}", mode="wb+") as w:
            w.write(content)

def copy_files(source_folder: str, destination_folder: str, remove: bool = True) -> None:
    if remove:
        delete_files(destination_folder)
    for element in os.listdir(source_folder):
        if os.path.isdir(f"{source_folder}/{element}"):
            os.makedirs(f"{destination_folder}/{element}")
            copy_files(f"{source_folder}/{element}", f"{destination_folder}/{element}", remove=False)
            continue
        process_file(element, source_folder, destination_folder)

        
def main():
    copy_files("./static", "./public")
main()
