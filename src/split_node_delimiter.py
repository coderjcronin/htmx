from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if text_type not in TextType:
        raise ValueError("Can not operate with non-enumerated TextType")
    
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