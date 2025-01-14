import re

from textnode import TextNode, TextType
from extractions import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    check_text_type(text_type)

    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            if node.text.count(delimiter) % 2 != 0:
                raise ValueError("Invalid Markdown syntax: unmatched delimiter found.")
            new_string_list = node.text.split(delimiter)
            for x in range(len(new_string_list)):
                if new_string_list[x] == '':
                    continue  # Skip empty parts
                if x % 2 == 0:
                    new_nodes.append(TextNode(new_string_list[x], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(new_string_list[x], text_type))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            new_string_list = re.split(r"(?<!!)\[.*?\]\(.*?\)", node.text)
            new_string_list.extend(extract_markdown_links(node.text))

            for item in new_string_list:
                if (isinstance(item, str)) and item != '':
                    new_nodes.append(TextNode(item, TextType.TEXT))
                elif (isinstance(item, tuple)):
                    new_nodes.append(TextNode(item[0], TextType.LINK, item[1]))
    
    return new_nodes



def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            new_string_list = re.split(r"!\[.*?\]\(.*?\)", node.text)
            new_string_list.extend(extract_markdown_images(node.text))

            for item in new_string_list:
                if (isinstance(item, str)) and item != '':
                    new_nodes.append(TextNode(item, TextType.TEXT))
                elif (isinstance(item, tuple)):
                    new_nodes.append(TextNode(item[0], TextType.IMAGE, item[1]))
    
    return new_nodes

def check_text_type(text_type):
    if text_type not in TextType:
        raise ValueError("Can not operate with non-enumerated TextType")
    