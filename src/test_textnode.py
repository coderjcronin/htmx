import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        node3 = TextNode("This is a new test", TextType.CODE, "https://google.com")
        node4 = TextNode("This is a new test", TextType.CODE, "https://google.com")
        self.assertEqual(node3, node4)

        node5 = TextNode("This shoudl fail", TextType.TEXT)
        node6 = TextNode("", TextType.TEXT)
        self.assertNotEqual(node5, node6)

        node7 = TextNode("This shoudl fail", TextType.TEXT, " ")
        self.assertNotEqual(node5, node7)

        node9 = TextNode("This shoudl fail", TextType.BOLD)
        self.assertNotEqual(node5, node9)



if __name__ == "__main__":
    unittest.main()