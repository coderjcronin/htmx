import unittest
from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter, split_nodes_image, split_nodes_link

#Global Variables
TEST_STRING_NORMAL = "This is my test string"
TEST_STRING_BOLD_SINGLE = "This is my **bold** test string"
TEST_STRING_TWO_WORDS = "This is my **bold test** string"
TEST_STRING_ITALIC = "This is my *italic* test string"
TEST_STRING_CODE = "This is my `code` test string"
TEST_STRING_EDGE_CASE_HALF_SENTENCE = "**This is my bold** test string"
TEST_STRING_EDGE_CASE_WHOLE_SENTENCE = "`This is my code test string`"
TEST_STRING_MALFORMED_BOLD = "This is my **bold test string"
TEST_STRING_ONE_IMAGE = "This is my test string with a ![image](https://fastly.picsum.photos/200.jpg)"
TEST_STRING_ONE_LINK = "This is my test string with a [link](https://boot.dev)"
TEST_STRING_TWO_LINKS = "This is my [test](https://google.com) string with [two](https://boot.dev) links."
TEST_STRING_TWO_IMAGES = "This is my ![test](https://fastly.picsum.photos/200.jpg) string with ![two](https://fastly.picsum.photos/200.jpg) images."
TEST_STRING_MIX_IMAGE_LINK = "This is my [test](https://boot.dev) string with mixed ![string](https://fastly.picsum.photos/200.jpg) markdown for link and image."
TEST_STRING_MIX_CODE_IMAGE = "This is my `code` and ![image](https://fastly.picsum.photos/200.jpg) test string."
TEST_STRING_MIXED_CODE_IMAGE = "You got ![`code`](https://fastly.picsum.photos/200.jpg) in my image!"


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

    # Extract a single link
    def test_split_single_link(self):
        self.test_node.text = TEST_STRING_ONE_LINK

        result = split_nodes_link([self.test_node])
        self.assertEqual(2, len(result), "Expected 2 nodes, did not get them.")
        self.assertTrue((isinstance(result[0], TextNode)) and (isinstance(result[1], TextNode)), "Expected both resulting nodes to be TextNode type, they're not.")
        self.assertEqual(TextType.LINK, result[1].text_type, "Second TextNode should be a link, it's not.")
        self.assertIsNot(None, result[1].url, "Expected content in link, got None")

    # Extract a single image
    def test_split_single_image(self):
        self.test_node.text = TEST_STRING_ONE_IMAGE

        result = split_nodes_image([self.test_node])
        self.assertEqual(2, len(result), "Expected 2 nodes, did not get them.")
        self.assertTrue((isinstance(result[0], TextNode)) and (isinstance(result[1], TextNode)), "Expected both resulting nodes to be TextNode type, they're not.")
        self.assertEqual(TextType.IMAGE, result[1].text_type, "Second TextNode should be a link, it's not.")
        self.assertIsNot(None, result[1].url, "Expected content in link, got None")

    # Test two links, iterates through to test nodes
    def test_split_two_links(self):
        self.test_node.text = TEST_STRING_TWO_LINKS

        result = split_nodes_link([self.test_node])
        self.assertEqual(5, len(result), "Expected 5 nodes, did not get them.")
        for node in result:
            self.assertTrue(isinstance(node, TextNode), "Expected all results to be TextNode, at least one was not.")
            self.assertIsNot('', node.text, "Expected content in TextNode text, got ''")
            if node.text_type == TextType.TEXT:
                self.assertIs('', node.url, "Expected '' for url for node with TextType.TEXT, got value")
            elif node.text_type == TextType.LINK:
                self.assertIsNot('', node.url, "Expected url value for node with TextType.LINK, got ''.")
            else:
                self.fail("Got unexpected TextNode with invalid TextType (should be TEXT or LINK)")


    # Test two images, iterates through to test nodes
    def test_split_two_images(self):
        self.test_node.text = TEST_STRING_TWO_IMAGES

        result = split_nodes_image([self.test_node])
        self.assertEqual(5, len(result), "Expected 5 nodes, did not get them.")
        for node in result:
            self.assertTrue(isinstance(node, TextNode), "Expected all results to be TextNode, at least one was not.")
            self.assertIsNot('', node.text, "Expected content in TextNode text, got ''")
            if node.text_type == TextType.TEXT:
                self.assertIs('', node.url, "Expected '' for url for node with TextType.TEXT, got value")
            elif node.text_type == TextType.IMAGE:
                self.assertIsNot('', node.url, "Expected url value for node with TextType.IMAGE, got ''.")
            else:
                self.fail("Got unexpected TextNode with invalid TextType (should be TEXT or IMAGE)")

    # Test mixed markdown for link and image
    def test_mixed_link_image(self):
        self.test_node.text = TEST_STRING_MIX_IMAGE_LINK

        #Test pull link first, this is most likely to fail
        result = split_nodes_link([self.test_node])
        self.assertEqual(3, len(result), "Expected 3 nodes, did not get them.")
        for node in result:
            self.assertTrue(isinstance(node, TextNode), "Expected all results to be TextNode, at least one was not.")
            self.assertIsNot('', node.text, "Expected content in TextNode text, got ''")
            if node.text_type == TextType.TEXT:
                self.assertIs('', node.url, "Expected '' for url for node with TextType.TEXT, got value")
            elif node.text_type == TextType.LINK:
                self.assertIsNot('', node.url, "Expected url value for node with TextType.LINK, got ''.")
            else:
                self.fail("Got unexpected TextNode with invalid TextType (should be TEXT or LINK)")       

        #Test pull image
        result = split_nodes_image([self.test_node])
        self.assertEqual(3, len(result), "Expected 3 nodes, did not get them.")
        for node in result:
            self.assertTrue(isinstance(node, TextNode), "Expected all results to be TextNode, at least one was not.")
            self.assertIsNot('', node.text, "Expected content in TextNode text, got ''")
            if node.text_type == TextType.TEXT:
                self.assertIs('', node.url, "Expected '' for url for node with TextType.TEXT, got value")
            elif node.text_type == TextType.IMAGE:
                self.assertIsNot('', node.url, "Expected url value for node with TextType.IMAGE, got ''.")
            else:
                self.fail("Got unexpected TextNode with invalid TextType (should be TEXT or IMAGE)")   

    # Test mix markdown for code and image
    def test_mix_code_image(self):
        self.test_node.text = TEST_STRING_MIX_CODE_IMAGE

        result = split_nodes_image([self.test_node])
        self.assertEqual(3, len(result), "Expected 3 nodes, did not get them.")
        for node in result:
            self.assertTrue(isinstance(node, TextNode), "Expected all results to be TextNode, at least one was not.")
            self.assertIsNot('', node.text, "Expected content in TextNode text, got ''")
            if node.text_type == TextType.TEXT:
                self.assertIs('', node.url, "Expected '' for url for node with TextType.TEXT, got value")
            elif node.text_type == TextType.IMAGE:
                self.assertIsNot('', node.url, "Expected url value for node with TextType.IMAGE, got ''.")
            else:
                self.fail("Got unexpected TextNode with invalid TextType (should be TEXT or IMAGE)")

        result = split_nodes_delimiter([self.test_node], "`", TextType.CODE)
        self.assertEqual(3, len(result), "Expected 3 nodes, did not get them.")
        for node in result:
            self.assertTrue(isinstance(node, TextNode), "Expected all results to be TextNode, at least one was not.")
            self.assertIsNot('', node.text, "Expected content in TextNode text, got ''")
            if node.text_type == TextType.TEXT:
                self.assertIs('', node.url, "Expected '' for url for node with TextType.TEXT, got value")
            elif node.text_type == TextType.CODE:
                self.assertIs('', node.url, "Expected '' for url for node with TextType.CODE, got value")
            else:
                self.fail("Got unexpected TextNode with invalid TextType (should be TEXT or CODE)")        
    
        

