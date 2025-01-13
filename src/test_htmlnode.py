import unittest

from htmlnode import HtmlNode

class TestHTMLNode(unittest.TestCase):
    def test_content(self):
        htmlnode1 = HtmlNode()
        self.assertIsNotNone(htmlnode1)

        htmlnode2 = HtmlNode("h1", "Title", "", { 'href' : 'http://coder-j.net' })
        self.assertEqual(' href="http://coder-j.net"', htmlnode2.props_to_html())

if __name__ == "__main__":
    unittest.main()