import unittest

from htmlnode import HtmlNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_content(self):
        htmlnode1 = HtmlNode()
        self.assertIsNotNone(htmlnode1)

        htmlnode2 = HtmlNode("h1", "Title", "", { 'href' : 'http://coder-j.net' })
        self.assertEqual(' href="http://coder-j.net"', htmlnode2.props_to_html())

class TestLeafNode(unittest.TestCase):
    def test_error(self):
        try:
            leafnode1 = LeafNode()
        except Exception as e:
            self.assertRaises(TypeError, e)

        try:
            leafnode1 = LeafNode('Test')
            leafnode1.value = None
            leafnode1.to_html()
        except ValueError as e:
            self.assertEqual(type(e), ValueError)
        else:
            self.fail("LeafNode value set to None does not raise ValueError")

    def test_content(self):
        test_string = "This is a test string"

        leafnode2 = LeafNode(test_string)
        self.assertEqual("This is a test string", leafnode2.to_html())

        leafnode3 = LeafNode(test_string, 'a', { 'href' : 'http://coder-j.net' })
        self.assertEqual('<a href="http://coder-j.net">This is a test string</a>', leafnode3.to_html())

class TestParentNode(unittest.TestCase):
    def test_error(self):
        try:
            parentnode1 = ParentNode()
        except Exception as e:
            self.assertRaises(TypeError, e)

        try:
            parentnode1 = ParentNode('p', LeafNode('Test'))
            parentnode1.tag = None
            parentnode1.to_html()
        except ValueError as e:
            self.assertEqual(type(e), ValueError)
        else:
            self.fail("ParentNode tag equal to None not raising ValueError")

    def test_content(self):
        test_string = "This is a test string"

        parentnode2 = ParentNode('p', (LeafNode(test_string), LeafNode(test_string, 'b'), LeafNode(test_string), LeafNode(test_string, 'a', { 'href' : 'http://coder-j.net'})))

        self.assertEqual(
            f'<p>{test_string}<b>{test_string}</b>{test_string}<a href="http://coder-j.net">{test_string}</a></p>',
            parentnode2.to_html()
            )

        

        

if __name__ == "__main__":
    unittest.main()