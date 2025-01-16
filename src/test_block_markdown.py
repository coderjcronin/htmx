from unittest import TestCase
from block_markdown import markdown_to_blocks

TEST_BLOCK_1 = """First



Second"""

TEST_BLOCK_2 = """
   Spaces   
   
   More spaces   
   """

TEST_BLOCK_3 = """# Header
Some text
    
* List 1
* List 2

Final paragraph"""

class test_block_markdown(TestCase):
    def test_block_one(self):
        results = markdown_to_blocks(TEST_BLOCK_1)

        self.assertEqual(2, len(results), "Expected 2 blocks")
        for result in results:
            self.assertFalse(result.startswith(' '), "Expected no leading whitespace")
            self.assertFalse(result.endswith(' '), "Expected no trailing whitespace")
            self.assertFalse(result == '', "Expected non-empty block")

    def test_block_two(self):
        results = markdown_to_blocks(TEST_BLOCK_2)

        self.assertEqual(2, len(results), "Expected 2 blocks")
        for result in results:
            self.assertFalse(result.startswith(' '), "Expected no leading whitespace")
            self.assertFalse(result.endswith(' '), "Expected no trailing whitespace")
            self.assertFalse(result == '', "Expected non-empty block")