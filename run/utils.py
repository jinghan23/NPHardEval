import xml.etree.ElementTree as ET
import ast


def parse_xml_to_dict(xml_string: str):
    """_summary_

    Args:
        xml_string (str): llm output string

    Returns:
        dict: dictionary of llm output
    """
    # Parse the XML string
    root = ET.fromstring(xml_string)

    # Find the 'final_answer' tag
    final_answer_element = root.find('final_answer')

    # Find the 'reasoning' tag
    reasoning_element = root.find('reasoning')

    # Convert the 'final_answer' tag to a dictionary
    output = ast.literal_eval(final_answer_element.text)
    print(reasoning_element.text)
    return output