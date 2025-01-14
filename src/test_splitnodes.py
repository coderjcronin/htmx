import unittest
from textnode import TextNode, TextType
from split_node_delimiter import split_nodes_delimiter

#Global Variables
TEST_STRING_NORMAL = "This is my test string"
TEST_STRING_BOLD_SINGLE = "This is my **bold** test string"
TEST_STRING_TWO_WORDS = "This is my **bold test** string"
TEST_STRING_ITALIC = "This is my *italic* test string"
TEST_STRING_CODE = "This is my `code` test string"
TEST_STRING_EDGE_CASE_HALF_SENTENCE = "**This is my bold** test string"
TEST_STRING_EDGE_CASE_WHOLE_SENTENCE = "`This is my code test string`"
TEST_STRING_MALFORMED_BOLD = "This is my **bold test string"


class test_textnode_split_delimiter(unittest.TestCase):
    def setUp(self):
        self.test_node = TextNode(TEST_STRING_NORMAL, TextType.TEXT)

    # Test to make sure TextNode with a TextType of anything other than .TEXT do not process (should be returned as is, no processing)
    def test_throw_back_of_nonText_node(self):
        self.test_node.text, self.test_node.text_type = TEST_STRING_BOLD_SINGLE, TextType.ITALIC
        results = split_nodes_delimiter([self.test_node], '**', TextType.BOLD)
        self.assertEqual(1, len(results), "split_nodes_delimiter returned a list of nodes (it should not of processed non-TextType.TEXT)")
        self.assertIsNot(TextType.BOLD, results[0].text_type, "split_nodes_delimiter returned TextType.Bold (it should not have processed the node)")

    # Test to make sure TextNode with no markup is simply returned.
    def test_normal(self):
        results = split_nodes_delimiter([self.test_node], '**', TextType.BOLD)
        self.assertEqual(1, len(results), "split_nodes_delimiter returned a list, there should of been no processing")
        self.assertIs(TextType.TEXT, results[0].text_type, "split_nodes_delimiter changed the TextType (should not have)")

    # Test bold processing
    def test_bold(self):
        self.test_node.text = TEST_STRING_BOLD_SINGLE

        results1 = split_nodes_delimiter([self.test_node], "**", TextType.BOLD)
        self.assertEqual(3, len(results1), "TextNode should have been split into 3 nodes")
        self.assertEqual(TextType.TEXT, results1[0].text_type, "The first TextNode should have been TextType.TEXT")
        self.assertEqual(TextType.TEXT, results1[2].text_type, "The last TextNode should have been TextType.TEXT")
        self.assertEqual(TextType.BOLD, results1[1].text_type, "Processed node should have been TextType.BOLD")

    # Test italic processing
    def test_italic(self):
        self.test_node.text = TEST_STRING_ITALIC

        results1 = split_nodes_delimiter([self.test_node], "*", TextType.ITALIC)
        self.assertEqual(3, len(results1), "TextNode should have been split into 3 nodes")
        self.assertEqual(TextType.TEXT, results1[0].text_type, "The first TextNode should have been TextType.TEXT")
        self.assertEqual(TextType.TEXT, results1[2].text_type, "The last TextNode should have been TextType.TEXT")
        self.assertEqual(TextType.ITALIC, results1[1].text_type, "Processed node should have been TextType.ITALIC")

    # Test code processing
    def test_code(self):
        self.test_node.text = TEST_STRING_CODE

        results1 = split_nodes_delimiter([self.test_node], "`", TextType.CODE)
        self.assertEqual(3, len(results1), "TextNode should have been split into 3 nodes")
        self.assertEqual(TextType.TEXT, results1[0].text_type, "The first TextNode should have been TextType.TEXT")
        self.assertEqual(TextType.TEXT, results1[2].text_type, "The last TextNode should have been TextType.TEXT")
        self.assertEqual(TextType.CODE, results1[1].text_type, "Processed node should have been TextType.CODE")
    
    # Test multiple words with markup (including edge cases)
    # Test two words
    def test_markup_two_words(self):
        self.test_node.text = TEST_STRING_TWO_WORDS

        results1 = split_nodes_delimiter([self.test_node], "**", TextType.BOLD)
        self.assertEqual(3, len(results1), "TextNode should have been split into 3 nodes")
        self.assertEqual(TextType.TEXT, results1[0].text_type, "The first TextNode should have been TextType.TEXT")
        self.assertEqual(TextType.TEXT, results1[2].text_type, "The last TextNode should have been TextType.TEXT")
        self.assertEqual(TextType.BOLD, results1[1].text_type, "Processed node should have been TextType.BOLD")
        self.assertEqual(2, len(results1[1].text.split(' ')), "There should be two words here.")

    # Test half the sentence (including very beginning, no whitespace)
    def test_half_sentence(self):
        self.test_node.text = TEST_STRING_EDGE_CASE_HALF_SENTENCE

        results1 = split_nodes_delimiter([self.test_node], "**", TextType.BOLD)
        self.assertEqual(2, len(results1), "TextNode should have been split into 2 nodes")
        self.assertEqual(TextType.BOLD, results1[0].text_type, "The first TextNode should have been TextType.TEXT")
        self.assertEqual(TextType.TEXT, results1[1].text_type, "The last TextNode should have been TextType.TEXT")
        self.assertEqual(4, len(results1[0].text.split(' ')), "There should be four words here.")

    #We shouldn't be doing this, but let's try to convert an entire .text, no leading or trailing whitespace
    def test_whole_sentence(self):
        self.test_node.text = TEST_STRING_EDGE_CASE_WHOLE_SENTENCE

        results1 = split_nodes_delimiter([self.test_node], "`", TextType.CODE)
        self.assertEqual(1, len(results1), "TextNode should not have been split into nodes")
        self.assertEqual(TextType.CODE, results1[0].text_type, "The first TextNode should have been TextType.CODE")
        self.assertEqual(6, len(results1[0].text.split(' ')), "There should be four words here.")

    # Error testing
    # Make sure we raise an error on malformed markup
    def test_malform_markup(self):
        self.test_node.text = TEST_STRING_MALFORMED_BOLD

        with self.assertRaises(ValueError, msg="Malformed markup should raise ValueError"):
            split_nodes_delimiter([self.test_node], "**", TextType.BOLD)

    # Make sure we raise an error on invalid markup type
    def test_invalid_markup_type(self):
        with self.assertRaises(ValueError, msg="Failed to screen invalid TextType for markup"):
            split_nodes_delimiter([self.test_node], "**", 'invalid')

