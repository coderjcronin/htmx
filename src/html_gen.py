import os
import pathlib
from block_to_html import markdown_to_html

def extract_title(markdown):
    lines = markdown.split('\n')

    for line in lines:
        if line.startswith('# '):
            return line.lstrip('# ')
    
    raise Exception("No valid title found")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    #if not os.path.exists(dir_path_content):
    #    raise ValueError("Invalid source path")
    #if not os.path.exists(template_path):
    #    raise ValueError("Invalid template path")
    #if not os.path.exists(dest_dir_path):
     #   raise ValueError("Invalid destination path")
    
    content_list = os.listdir(dir_path_content)
    for item in content_list:
        if not pathlib.Path(dir_path_content + '/' + item).is_dir():
            if item.endswith('.md'):
                destination_file = dest_dir_path + '/' + item.rstrip('.md') + '.html'
                print(pathlib.Path(item))
                generate_page(dir_path_content + '/' + item, template_path, destination_file )
            else:
                print(f"Invalid file found, {item}, skipping...")
        else: #assume it's a directory
            new_destination = dest_dir_path + '/' + item
            new_source = dir_path_content + '/' + item
            os.makedirs(new_destination)
            generate_pages_recursive(new_source, template_path, new_destination)

def generate_page(from_path, template_path, dest_path):

    #check our template and source
    if not os.path.exists(from_path):
        raise ValueError("Invalid source file path")
    if not os.path.exists(template_path):
        raise ValueError("Invalid tempalte path")
    
    #check destination, it shouldn't exist
    if os.path.exists(dest_path):
        raise ValueError("Destination file already exists")
    
    with open(from_path) as f:
        source_content = f.read()
    
    with open(template_path) as f:
        template_content = f.read()

    page_title = extract_title(source_content)
    page_content = markdown_to_html(source_content)

    template_lines = template_content.split('\n')
    new_page_lines = []
    for line in template_lines:
        new_line = line.replace('{{ Title }}', page_title).replace('{{ Content }}', page_content.to_html())
        new_page_lines.append(new_line)
    new_page = "\n".join(new_page_lines)
   
    with open(dest_path, 'w') as f:
        f.write(new_page)

    # This should be last...
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
