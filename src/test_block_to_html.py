import unittest

from block_to_html import * 

#GLOBAL VARIABLES
TEST_STRING = 'This is a test'
TEST_URL = 'https://arstechnica.com'
TEST_IMAGE = 'https://cdn.arstechnica.net/wp-content/uploads/2025/01/GettyImages-1244585198.jpg'
TEST_STRING_FROM_ASSIGNMENT = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
TEST_STRING_STRIPPED = "This is text with an italic word and a code block and an obi wan image and a link"
TEST_CASE_1 = '''
# Header

```
import re

def test_filter(content):
    return re.search(r'!\\[(.*?)\\], content)
```

* This is a pain
* OMG so much typing!

![Random Image](https://picsum.photos/200/300)

This is a **bold** paragraph with *emphasis* and [inline](https://boot.dev) links.'''

class test_textnode_to_html_conversion(unittest.TestCase):
    def test_error(self):
        textnodex = TextNode('Test', TextType.TEXT)
        try:
            textnodex.text_type = None
            textx = text_node_to_html_node(textnodex)
        except Exception as e:
            self.assertEqual(type(e), ValueError)
        else:
            self.fail("text_node_to_html_node did not raise ValueError with invalid TextType ENUM")
    
    def test_text_conversion(self):
        textnode1 = TextNode(TEST_STRING, TextType.TEXT)

        #Test TextType.NORMAL (no tag)
        test1 = text_node_to_html_node(textnode1)
        self.assertIsInstance(test1, LeafNode, "text_node_to_html_node did not return a LeafNode object")
        self.assertEqual(TEST_STRING, test1.value, "Test string with TextType.TEXT did not convert properly to LeafNode value")
        self.assertIsNone(test1.tag, "TextType.TEXT should not convert with a tag (should be None)")

    def test_italic_conversion(self):
        textnode2 = TextNode(TEST_STRING, TextType.ITALIC)
        
        #Test TextType.ITALIC (i tag)
        test2 = text_node_to_html_node(textnode2)
        self.assertIsInstance(test2, LeafNode, "text_node_to_html_node did not return a LeafNode object")
        self.assertEqual(TEST_STRING, test2.value, "Test string with TextType.ITALIC did not convert properly to LeafNode value")
        self.assertEqual('i', test2.tag, "TextType.ITALIC did not convert with 'i' tag")

    def test_code_conversion(self):
        textnode3 = TextNode(TEST_STRING, TextType.CODE)
        
        #Test TextType.CODE (code tag)
        test3 = text_node_to_html_node(textnode3)
        self.assertIsInstance(test3, LeafNode, "text_node_to_html_node did not return a LeafNode object")
        self.assertEqual(TEST_STRING, test3.value, "Test string with TextType.CODE did not convert properly to LeafNode value")
        self.assertEqual('code', test3.tag, "TextType.CODE did not convert with 'code' tag")

    def test_bold_conversion(self):
        textnode4 = TextNode(TEST_STRING, TextType.BOLD)

        #Test TextType.BOLD (b tag)
        test4 = text_node_to_html_node(textnode4)
        self.assertIsInstance(test4, LeafNode, "text_node_to_html_node did not return a LeafNode object")
        self.assertEqual(TEST_STRING, test4.value, "Test string with TextType.BOLD did not convert properly to LeafNode value")
        self.assertEqual('b', test4.tag, "TextType.BOLD did not convert with 'b' tag")      

    def test_link_conversion(self):
        textnode5 = TextNode(TEST_STRING, TextType.LINK, TEST_URL)

        #Test TextType.LINK (a tag)
        test5 = text_node_to_html_node(textnode5)
        self.assertIsInstance(test5, LeafNode, "text_node_to_html_node did not return a LeafNode object")
        self.assertEqual(TEST_STRING, test5.value, "Test string with TextType.LINK did not convert properly to LeafNode value")
        self.assertEqual('a', test5.tag, "TextType.LINK did not convert with 'a' tag")
        self.assertEqual({ 'href' : TEST_URL }, test5.props, "TextType.LINK did not convert with prop of href and URL")

    def test_image_conversion(self):
        textnode6 = TextNode(TEST_STRING, TextType.IMAGE, TEST_IMAGE)

        #Test TextType.IMAGE (img tag)
        test6 = text_node_to_html_node(textnode6)
        self.assertIsInstance(test6, LeafNode, "text_node_to_html_node did not return a LeafNode object")
        self.assertEqual("", test6.value, "Test string with TextType.IMAGE did not convert properly to LeafNode value (should be empty string)")
        self.assertEqual('img', test6.tag, "TextType.IMAGE did not convert with 'img' tag")
        self.assertEqual({ 'src' : TEST_IMAGE, 'alt' : TEST_STRING }, test6.props, "TextType.IMAGE did not convert with props of src and alt")

    def test_text_to_textnodes(self):
        results = text_to_textnodes(TEST_STRING_FROM_ASSIGNMENT)
        
        reconstruct_string = ""

        for result in results:
            self.assertTrue(isinstance(result, TextNode), "Expected TextNode type")
            self.assertTrue(result.text_type in TextType, "Expected TextNode text_type to be enumerated in TextType")
            if result.text_type == TextType.IMAGE or result.text_type == TextType.LINK:
                self.assertIsNotNone(result.url, "Expected results with type LINK or IMAGE to have URL, had None")
            reconstruct_string += result.text

        self.assertEqual(reconstruct_string, TEST_STRING_STRIPPED, "Expected reconstructed string from TextNodes")



