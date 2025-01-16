from htmlnode import ParentNode, LeafNode, HtmlNode
from textnode import TextNode
from split_nodes import split_nodes_delimiter, split_nodes_image, split_nodes_link
from local_types import BlockType, TextType
from block_markdown import markdown_to_blocks, block_to_block_type

# Globals
PATTERNS = [
    ( '**', TextType.BOLD),
    ( '*', TextType.ITALIC),
    ( '`', TextType.CODE)
]

def markdown_to_html(markdown):
    child_nodes = []

    #Split markdown into blocks
    blocks = markdown_to_blocks(markdown)

    #Start processing these bad boys
    for block in blocks:
        child_nodes.append(block_to_html(block))

    return ParentNode( 'div', child_nodes)

def block_to_html(block):
    block_type = block_to_block_type(block)
    match (block_type):
        case BlockType.HEADING:
            return heading_to_block(block)
        case BlockType.ULIST:
            return ParentNode( 'ul' , text_to_list(block))
        case BlockType.OLIST:
            return ParentNode( 'ol', text_to_list(block))
        case BlockType.CODE:
            return ParentNode( 'pre' , [LeafNode(block.strip('`\n'), 'code')])
        case BlockType.QUOTE:
            return ParentNode( 'blockquote' , [LeafNode(strip_quote_markdown(block))])
        case _: # BlockType.Paragraph and catchall... might need to cleanup
            return ParentNode( 'p' , text_to_children(block))


def text_to_children(text):
    # Take in text, convert to textnode and process, return list of leaf nodes to be appended to parent html node
    # Assume it's been processed to get rid of excess whitespace and other nonsense
    new_text_nodes = text_to_textnodes(text)
    children = []
    for text_node in new_text_nodes:
        children.append(text_node_to_html_node(text_node))

    return children

def text_to_list(text):
    lines = text.split('\n')
    children = []

    for line in lines:
        children.append(ParentNode( 'li', text_to_children(line.lstrip('0123456789.*- '))))

    return children

def heading_to_block(heading):
    level = 0

    for character in heading:
        if character == "#":
            level += 1
        else:
            break

    if level + 1 >= len(heading) or level > 6:
        raise ValueError(f"{level} is invalid heading value, check markdown")
    else:
        return LeafNode( heading[level+1:], f"h{level}")

def strip_quote_markdown(text):
    lines = text.split('\n')
    new_lines = []
    for line in lines:
        new_lines.append(line.lstrip('> '))
    return "\n".join(new_lines)

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
        
def text_to_textnodes(text):
    temp_node = [TextNode(text, TextType.TEXT)]

    temp_node = split_nodes_image(temp_node)
    temp_node = split_nodes_link(temp_node)

    for delimiter, text_type in PATTERNS:
        temp_node = split_nodes_delimiter(temp_node, delimiter, text_type)

    return temp_node