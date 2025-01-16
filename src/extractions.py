import re

def extract_markdown_images(text):
    if text == "" or text == []:
        return
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    if text == "" or text == []:
        return
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
