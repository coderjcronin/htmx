
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
        for prop in self.props:
             temp_string += f" {prop}=\"{self.props[prop]}\""
        
        return temp_string
    
    def __repr__(self):
        return f"{self.tag}\n - value {self.value}\n - children {self.children}\n - props {self.props}"