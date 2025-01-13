from textnode import *
from htmlnode import *

def main():
    mighty_test = TextNode("This is a test text node", TextType.ITALIC, "http://coder-j.net")
    print(mighty_test)

    mighty_html = HtmlNode("h1", "A Title", "", { 'font' : 'Arial', 'weight' : 'bold}'})
    print(mighty_html)

main()