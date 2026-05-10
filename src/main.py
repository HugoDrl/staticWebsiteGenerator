import os
import sys

from process_html import extract_title, markdown_to_html_node

def delete_files(folder: str) -> None:
    if not os.path.exists(folder):
        return
    for element in os.listdir(folder):
        if os.path.isdir(f"{folder}/{element}"):
            delete_files(f"{folder}/{element}")
            continue
        os.remove(f"{folder}/{element}")
    os.rmdir(folder)

def process_file(file: str, source_folder: str, destination_folder: str):
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

def generate_page(from_path: str, template_path: str, dest_path: str, base_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        content = f.read()
    with open(template_path) as t:
        template = t.read()
    html = markdown_to_html_node(content).to_html()
    html = html.replace('href="/', f'href="{base_path}')
    html = html.replace('src="/', f'src="{base_path}')
    title = extract_title(content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    os.makedirs("/".join(dest_path.split("/")[:-1]), exist_ok=True)
    with open(dest_path, "w+") as f:
        f.write(template)

def generate_website(from_folder: str, template_path: str, dest_folder: str, base_path: str) -> None:
    if not os.path.exists(from_folder):
        raise FileExistsError(f"{from_folder} not found")
    for element in os.listdir(from_folder):
        if os.path.isdir(f"{from_folder}/{element}"):
            os.mkdir(f"{dest_folder}/{element}") 
            generate_website(f"{from_folder}/{element}", template_path, f"{dest_folder}/{element}", base_path)
            continue
        generate_page(f"{from_folder}/{element}", template_path, f"{dest_folder}/{element.replace(".md", ".html")}", base_path)

def main():
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        base_path = "/"
    copy_files("./static", "./docs")
    generate_website(
            from_folder="./content",
            template_path="./template.html",
            dest_folder="./docs",
            base_path=base_path,
            )
main()
