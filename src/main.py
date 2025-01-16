# Imports
from textnode import *
from htmlnode import *
from block_to_html import *
from extractions import extract_markdown_images, extract_markdown_links
from split_nodes import split_nodes_delimiter, split_nodes_link, split_nodes_image

TEST_CASE_1 = '''# Header

```
import re
def test_filter(content):
    return re.search(r'!\\[(.*?)\\], content)
```

* This is a pain
* OMG so much typing!

![Random Image](https://picsum.photos/200/300)

This is a **bold** paragraph with *emphasis* and [inline](https://boot.dev) links.'''

def main():
    print(markdown_to_html(TEST_CASE_1))


                
main()