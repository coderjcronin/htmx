from local_types import BlockType

def markdown_to_blocks(markdown):
    lines = markdown.split('\n')
    for i, line in enumerate(lines):
        if line.isspace():
            lines[i] = ''
    cleaned_markdown = "\n".join(lines)
    blocks = cleaned_markdown.split('\n\n')

    cleaned_blocks = []
    for block in blocks:
        clean_block = block.strip()
        if clean_block != '':
            cleaned_blocks.append(clean_block)

    return cleaned_blocks

def block_to_block_type(incoming_block):
    lines = incoming_block.split('\n')

    if incoming_block.startswith(("#", "##", "###", "####", "#####", "######")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if incoming_block.startswith('>'):
        for line in lines:
            if not line.startswith('>'):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if incoming_block.startswith('* '):
        for line in lines:
            if not line.startswith('* '):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if incoming_block.startswith('- '):
        for line in lines:
            if not line.startswith('- '):
                return BlockType.PARAGRAPH
        return BlockType.ULISTLIST
    if incoming_block.startswith('1. '):
        x = 1
        for line in lines:
            if not line.startswith(f"{x}. "):
                return BlockType.PARAGRAPH
            x += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH
    