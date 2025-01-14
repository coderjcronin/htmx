from textnode import *
from htmlnode import *
from extractions import extract_markdown_images, extract_markdown_links
from split_nodes import split_nodes_delimiter, split_nodes_link, split_nodes_image

def main():
    pass

def text_node_to_html_node(text_node):
    match (text_node.text_type):
        case (TextType.TEXT):
            return LeafNode(text_node.text)
        case (TextType.BOLD):
            return LeafNode(text_node.text, 'b')
        case (TextType.ITALIC):
            return LeafNode(text_node.text, 'i')
        case (TextType.CODE):
            return LeafNode(text_node.text, 'code')
        case (TextType.IMAGE):
            return LeafNode("", 'img', { 'src' : text_node.url, 'alt' : text_node.text })
        case (TextType.LINK):
            return LeafNode(text_node.text, 'a', { 'href' : text_node.url })
        case _:
            raise ValueError("TextNode text type does not match ENUM list")
                
main()