import unittest

from html_gen import *

#Global Variables
TEST_PATH_1 = "./content/index.md"
TEST_PATH_2 = "./template/template.html"
TEST_PATH_3 = "./public/index.html"
TEST_PATH_4 = "/invalid/place.lnk"
TEST_CASE_1 = '''
# Header

## Header 2

```
import re
def test_filter(content):
    return re.search(r'!\\[(.*?)\\], content)
```

* This is a pain
* OMG so much typing!

![Random Image](https://picsum.photos/200/300)

This is a **bold** paragraph with *emphasis* and [inline](https://boot.dev) links.'''

TEST_CASE_2 = '''
## Header 2

```
import re
def test_filter(content):
    return re.search(r'!\\[(.*?)\\], content)
```

* This is a pain
* OMG so much typing!

![Random Image](https://picsum.photos/200/300)

This is a **bold** paragraph with *emphasis* and [inline](https://boot.dev) links.'''





class test_html_gen(unittest.TestCase):
    def test_gen_header(self):
        test_case = extract_title(TEST_CASE_1)
        self.assertEqual('Header', test_case, "Expected \'Header\' for extract_title()")

        with self.assertRaises(Exception, msg="Expected Exception for not finding H1"):
            test_case = extract_title(TEST_CASE_2)

    def test_paths(self):
        with self.assertRaises(ValueError, msg="Expected ValueError for invalid source path"):
            generate_page(TEST_PATH_4, TEST_PATH_2, TEST_PATH_3)
        
        with self.assertRaises(ValueError, msg="Expected ValueError for invalid template path"):
            generate_page(TEST_PATH_1, TEST_PATH_4, TEST_PATH_3)