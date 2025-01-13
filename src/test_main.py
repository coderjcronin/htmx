
import unittest
import main
from textnode import TextNode, TextType
from htmlnode import HtmlNode, LeafNode, ParentNode

#Test Variables
test_string = 'This is a test'
test_url = 'https://arstechnica.com'
test_image = 'https://cdn.arstechnica.net/wp-content/uploads/2025/01/GettyImages-1244585198.jpg'

class test_textnode_to_html_conversion(unittest.TestCase):
    def test_error(self):
        textnodex = TextNode('Test', TextType.TEXT)
        try:
            textnodex.text_type = None
            textx = main.text_node_to_html_node(textnodex)
        except Exception as e:
            self.assertEqual(type(e), ValueError)
        else:
            self.fail("text_node_to_html_node did not raise ValueError with invalid TextType ENUM")
    
    def test_text_conversion(self):
        textnode1 = TextNode(test_string, TextType.TEXT)

        #Test TextType.NORMAL (no tag)
        test1 = main.text_node_to_html_node(textnode1)
        self.assertIsInstance(test1, LeafNode, "text_node_to_html_node did not return a LeafNode object")
        self.assertEqual(test_string, test1.value, "Test string with TextType.TEXT did not convert properly to LeafNode value")
        self.assertIsNone(test1.tag, "TextType.TEXT should not convert with a tag (should be None)")

    def test_italic_conversion(self):
        textnode2 = TextNode(test_string, TextType.ITALIC)
        
        #Test TextType.ITALIC (i tag)
        test2 = main.text_node_to_html_node(textnode2)
        self.assertIsInstance(test2, LeafNode, "text_node_to_html_node did not return a LeafNode object")
        self.assertEqual(test_string, test2.value, "Test string with TextType.ITALIC did not convert properly to LeafNode value")
        self.assertEqual('i', test2.tag, "TextType.ITALIC did not convert with 'i' tag")

    def test_code_conversion(self):
        textnode3 = TextNode(test_string, TextType.CODE)
        
        #Test TextType.CODE (code tag)
        test3 = main.text_node_to_html_node(textnode3)
        self.assertIsInstance(test3, LeafNode, "text_node_to_html_node did not return a LeafNode object")
        self.assertEqual(test_string, test3.value, "Test string with TextType.CODE did not convert properly to LeafNode value")
        self.assertEqual('code', test3.tag, "TextType.CODE did not convert with 'code' tag")

    def test_bold_conversion(self):
        textnode4 = TextNode(test_string, TextType.BOLD)

        #Test TextType.BOLD (b tag)
        test4 = main.text_node_to_html_node(textnode4)
        self.assertIsInstance(test4, LeafNode, "text_node_to_html_node did not return a LeafNode object")
        self.assertEqual(test_string, test4.value, "Test string with TextType.BOLD did not convert properly to LeafNode value")
        self.assertEqual('b', test4.tag, "TextType.BOLD did not convert with 'b' tag")      

    def test_link_conversion(self):
        textnode5 = TextNode(test_string, TextType.LINK, test_url)

        #Test TextType.LINK (a tag)
        test5 = main.text_node_to_html_node(textnode5)
        self.assertIsInstance(test5, LeafNode, "text_node_to_html_node did not return a LeafNode object")
        self.assertEqual(test_string, test5.value, "Test string with TextType.LINK did not convert properly to LeafNode value")
        self.assertEqual('a', test5.tag, "TextType.LINK did not convert with 'a' tag")
        self.assertEqual({ 'href' : test_url }, test5.props, "TextType.LINK did not convert with prop of href and URL")

    def test_image_conversion(self):
        textnode6 = TextNode(test_string, TextType.IMAGE, test_image)

        #Test TextType.IMAGE (img tag)
        test6 = main.text_node_to_html_node(textnode6)
        self.assertIsInstance(test6, LeafNode, "text_node_to_html_node did not return a LeafNode object")
        self.assertEqual("", test6.value, "Test string with TextType.IMAGE did not convert properly to LeafNode value (should be empty string)")
        self.assertEqual('img', test6.tag, "TextType.IMAGE did not convert with 'img' tag")
        self.assertEqual({ 'src' : test_image, 'alt' : test_string }, test6.props, "TextType.IMAGE did not convert with props of src and alt")