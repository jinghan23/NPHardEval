import xml.etree.ElementTree as ET
import ast


def append_root_tags(string):
    if not string.strip().startswith("<root>"):
        string = "<root>\n" + string
    if not string.strip().endswith("</root>"):
        string += "\n</root>"
    return string

def parse_xml_to_dict(xml_string):
    try:
        # Parse the XML string
        root = ET.fromstring(xml_string)

        # Find the 'final_answer' tag
        final_answer_element = root.find('final_answer')

        # Find the 'reasoning' tag
        reasoning_element = root.find('reasoning')
    except:
        try:
            assert '<final_answer>' in xml_string
            assert '</final_answer>' in xml_string
            assert '<reasoning>' in xml_string 
            assert '</reasoning>' in xml_string
            final_answer_start = xml_string.index('<final_answer>') + len('<final_answer>') 
            final_answer_end = xml_string.index('</final_answer>')
            reasoning_start = xml_string.index('<reasoning>') + len('<reasoning>')
            reasoning_end = xml_string.index('</reasoning>')
            final_answer_element  = xml_string[final_answer_start:final_answer_end]
            reasoning_element = xml_string[reasoning_start:reasoning_end]
        except:
            final_answer_element = ''
            reasoning_element = ''

    return final_answer_element, reasoning_element