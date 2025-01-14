import unittest

from extractions import extract_markdown_links, extract_markdown_images

#GLOBAL VARIABLES
TEST_STRING_WITH_ONE_IMAGE = "This is a single ![image](https://picsum.photos/200.png) test"
TEST_STRING_WITH_TWO_IMAGES = "This is two ![image1](https://picsum.photos/200.png) image ![image2](https://picsum.photos/150.png) test"
TEST_STRING_WITH_MALFORMED_IMAGE = "This is a test ![whoops(https://picsum.photos/200) string with bad markdown"
TEST_STRING_WITH_ONE_LINK = "This is a single [link](https://boot.dev) test"
TEST_STRING_WITH_TWO_LINKS = "This is a double [link](https://boot.dev) text [test](https://google.com)"
TEST_STRING_WITH_MALFORMED_LINK = "This is a test with a [bad](https://boot.dev link markdown"

class test_extractions(unittest.TestCase):
    # Test one image
    def test_single_image(self):
        result = extract_markdown_images(TEST_STRING_WITH_ONE_IMAGE)
        self.assertEqual(1, len(result), "List should be single item")
        self.assertTrue(isinstance(result[0], tuple), "Result should be tuple")
        self.assertEqual(2, len(result[0]), "Result tuple should only have two elements (alt text and image)")

    # Test two images
    def test_two_image(self):
        result = extract_markdown_images(TEST_STRING_WITH_TWO_IMAGES)
        self.assertEqual(2, len(result), "List should be two items")
        self.assertEqual(2, len(result[0]), "Result tuple 1 should only have two elements (alt text and image)")
        self.assertEqual(2, len(result[1]), "Result tuple 2 should only have two elements (alt text and image)")

    # Test one link
    def test_single_link(self):
        result = extract_markdown_links(TEST_STRING_WITH_ONE_LINK)
        self.assertEqual(1, len(result), "List should be single item")
        self.assertTrue(isinstance(result[0], tuple), "Result should be tuple")
        self.assertEqual(2, len(result[0]), "Result tuple should only have two elements (text and link)")

    # Test two links
    def test_two_links(self):
        result = extract_markdown_links(TEST_STRING_WITH_TWO_LINKS)
        self.assertEqual(2, len(result), "List should be single items")
        self.assertTrue(isinstance(result[0], tuple), "Result should be tuple")
        self.assertEqual(2, len(result[0]), "Result 1 tuple should only have two elements (text and link)")
        self.assertEqual(2, len(result[1]), "Result 2 tuple should only have two elements (text and link)")

    # Test malformed image markdown
    def test_malformed_image(self):
        result = extract_markdown_images(TEST_STRING_WITH_MALFORMED_IMAGE)
        self.assertEqual(0, len(result), "There should be no results")

    # Test malformed link markdown
    def test_malformed_link(self):
        result = extract_markdown_links(TEST_STRING_WITH_MALFORMED_LINK)
        self.assertEqual(0, len(result), "There should be no results")