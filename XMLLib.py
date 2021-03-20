import xml.etree.ElementTree as XML


def register_namespaces(xml_namespace_list):
    for name_space in xml_namespace_list:
        XML.register_namespace(name_space["Prefix"], name_space["URI"])


def correct_xml_header(xml_string):
    new_xml_string = xml_string.replace("<?xml version='1.0' encoding='utf-8'?>",
                                        '<?xml version="1.0" encoding="utf-8"?>')
    return new_xml_string


class XmlDocument:
    def __init__(self, file):
        self.tree_object = XML.parse(file)
        self.root = self.tree_object.getroot()

    def get_element(self, tag_name):
        # Functionality: Finds the first given element in the tree and returns it
        # Hints: TreeElements have two main attributes: .text = content, .tag = tag
        found_element = None
        for element in self.tree_object.iter():
            if tag_name in element.tag:
                found_element = element
                break
        return found_element

    def change_element_content(self, name, content):
        # Functionality: searches for the given element in the tree and changes its content
        # Results = 0 - OK, 1 - NOK
        result = 1
        element = self.get_element(name)
        if element is not None:
            element.text = str(content)
            print("Element " + name + " updated with value " + str(content))
            result = 0
        return result

    def get_as_file(self, file_name):
        file = self.tree_object.write(file_name, encoding='utf-8', xml_declaration=True)
        return file




