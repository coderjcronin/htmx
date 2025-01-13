import unittest

from htmlnode import HtmlNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_content(self):
        htmlnode1 = HtmlNode()
        self.assertIsNotNone(htmlnode1)

        htmlnode2 = HtmlNode("h1", "Title", "", { 'href' : 'http://coder-j.net' })
        self.assertEqual(' href="http://coder-j.net"', htmlnode2.props_to_html())

class TestLeafNode(unittest.TestCase):
    def test_content(self):
        
        test_string = "This is a test string"
        try:
            leafnode1 = LeafNode()
        except Exception as e:
            self.assertRaises(TypeError, e)

        leafnode2 = LeafNode(test_string)
        self.assertEqual("This is a test string", leafnode2.to_html())

        leafnode3 = LeafNode(test_string, 'a', { 'href' : 'http://coder-j.net' })
        self.assertEqual('<a href="http://coder-j.net">This is a test string</a>', leafnode3.to_html())

if __name__ == "__main__":
    unittest.main()