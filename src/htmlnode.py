
class HtmlNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        temp_string = ""
        if self.props != None:
            for prop in self.props:
                temp_string += f" {prop}=\"{self.props[prop]}\""

        return temp_string
    
    def __repr__(self):
        return f"{self.tag}\n - value {self.value}\n - children {self.children}\n - props {self.props}"
    
class LeafNode(HtmlNode):
    def __init__(self, value, tag = None, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNode has no value.")
        if self.tag == None:
            return f"{self.value}"
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
class ParentNode(HtmlNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNode has no value")
        elif self.children == None:
            raise ValueError("ParentNode has no children.")
        else:
            new_string = f"<{self.tag}>"
            for tag in self.children:
                new_string += tag.to_html()
            new_string += f"</{self.tag}>"

            return new_string
