import xml.etree.ElementTree as ET
import ast

def parse_xml_to_dict(xml_string):
    try:
        assert '<final_answer>' in xml_string
        assert '</final_answer>' in xml_string
        #assert '<reasoning>' in xml_string 
        #assert '</reasoning>' in xml_string
        final_answer_start = xml_string.index('<final_answer>') + len('<final_answer>') 
        final_answer_end = xml_string.index('</final_answer>')
        #reasoning_start = xml_string.index('<reasoning>') + len('<reasoning>')
        #reasoning_end = xml_string.index('</reasoning>')
        final_answer_element  = xml_string[final_answer_start:final_answer_end].rstrip().strip().rstrip()
        assert '{' in final_answer_element
        assert '}' in final_answer_element
        dic_start = final_answer_element.index('{')
        dic_end = final_answer_element.index('}')
        final_answer_element = final_answer_element[dic_start:dic_end+1].rstrip().strip().rstrip()
        reasoning_element = xml_string
        #reasoning_element = xml_string[reasoning_start:reasoning_end].rstrip().strip().rstrip()
        try:
            final_answer_element = ast.literal_eval(final_answer_element)
        except:
            final_answer_element = ''
    except:
        final_answer_element = ''
        reasoning_element = ''

    return final_answer_element, reasoning_element
