import unittest
from textnode import TextNode, TextType
from split_node_delimiter import split_nodes_delimiter

#Global Variables
test_string_normal = "This is my test string"
test_string_bold1 = "This is my **bold** test string"
test_string_bold2 = "This is my **bold test** string"
test_string_bold3 = "**This is my bold** test string"
test_string_bold4 = "This is my **bold test string**"
test_string_bold_broken1 = "This is my **broken test string"
test_string_bold_broken2 = "This is **my** **broken test string"
test_string_italic1 = "This is my *italic* test string"
test_string_italic2 = "This is my *italic test* string"
test_string_italic_broken1 = "This is my *broken test string"
test_string_italic_broken2 = "This is *my* *broken test string"
test_string_code1 = "This is my `code` test string"
test_string_code2 = "This is my `code test` string"
test_string_code_broken1 = "This is my `broken string"
test_string_code_broken2 = "This is `my` `broken string"

class test_textnode_split_delimiter(unittest.TestCase):
    def test_throw_back_of_nonText_node(self):
        throw_test_node = TextNode(test_string_bold1, TextType.ITALIC)
        results = split_nodes_delimiter([throw_test_node], '**', TextType.BOLD)
        self.assertEqual(1, len(results), "split_nodes_delimiter returned a list of nodes (it should not of processed non-TextType.TEXT)")
        self.assertIsNot(TextType.BOLD, results[0].text_type, "split_nodes_delimiter returned TextType.Bold (it shoudl not have processed the node)")

    def test_normal(self):
        normal_node = TextNode(test_string_normal, TextType.TEXT)
        results = split_nodes_delimiter([normal_node], '**', TextType.BOLD)
        self.assertEqual(1, len(results), "split_nodes_delimiter returned a list, there should of been no processing")
        self.assertIs(TextType.TEXT, results[0].text_type, "split_nodes_delimiter changed the TextType (should not have)")

        def test_bold(self):
            bold_node1 = TextNode(test_string_bold1, TextType.TEXT)
            bold_node2 = TextNode(test_string_bold2, TextType.TEXT)
            bold_node3 = TextNode(test_string_bold3, TextType.TEXT)
            bold_node4 = TextNode(test_string_bold4, TextType.TEXT)

            #Try single string first. We should get 3 TextNodes, first and last should be TextType.TEXT and middle should be TextType.BOLD
            results1 = split_nodes_delimiter([bold_node1], "**", TextType.BOLD)
            self.assertEqual(3, len(results1), "TextNode should have been split into 3 nodes")
            self.assertEqual(TextType.TEXT, results1[0].text_type, "The first TextNode should have been TextType.TEXT")
            self.assertEqual(TextType.TEXT, results1[2].text_type, "The last TextNode should have been TextType.TEXT")
            self.assertEqual(TextType.BOLD, results1[1].text_type, "Processed node should have been TextType.BOLD")

            #Now let's throw 2 in, one will have a white space. 6 total TextNodes, 0/2/3/5 should be TextType.TEXT, 1/4 should be TextType.BOLD, 4 should be two words
            results1 = split_nodes_delimiter([bold_node1, bold_node2], "**", TextType.BOLD)
            self.assertEqual(6, len(results1), "TextNodes should have been split into 6 nodes")
            self.assertEqual(TextType.TEXT, results1[0].text_type, "The first TextNode should have been TextType.TEXT")
            self.assertEqual(TextType.TEXT, results1[2].text_type, "The third TextNode should have been TextType.TEXT")
            self.assertEqual(TextType.TEXT, results1[3].text_type, "The fourth TextNode should have been TextType.TEXT")
            self.assertEqual(TextType.TEXT, results1[5].text_type, "The last TextNode should have been TextType.TEXT")
            self.assertEqual(TextType.BOLD, results1[1].text_type, "Processed node should have been TextType.BOLD")
            self.assertEqual(TextType.BOLD, results1[4].text_type, "Processed node should have been TextType.BOLD")
            self.assertEqual(2, len(results1[4].text.split(" ")), "Result of two word conversion was not two words")

            #Great, now edge cases. 2 words, one with markup in beginning to mid, one with markup mid to end. We should get 4 nodes, 2 bold and 2 normal
            results1 = split_nodes_delimiter([bold_node3, bold_node4], "**", TextType.BOLD)
            self.assertEqual(4, len(results1), "TextNodes should have been split into 4 nodes")
            self.assertEqual(TextType.BOLD, results1[0].text_type, "The first TextNode should have been TextType.BOLD")
            self.assertEqual(TextType.TEXT, results1[1].text_type, "The second TextNode should have been TextType.TEXT")
            self.assertEqual(TextType.TEXT, results1[2].text_type, "The third TextNode should have been TextType.TEXT")
            self.assertEqual(TextType.BOLD, results1[3].text_type, "The last node should have been TextType.BOLD")

            #Finally, test the broken ones
            with self.assertRaises(ValueError, msg="Malformed markup should raise ValueError"):
                split_nodes_delimiter([test_string_bold_broken1], "**", TextType.BOLD)
            
            with self.assertRaises(ValueError, msg="Malformed markup should raise ValueError"):
                split_nodes_delimiter([test_string_bold_broken2], "**", TextType.BOLD)

