import xml.etree.ElementTree as ET
def parse_xml_to_dict(xml_string):
    """Parses the XML string returned by the model.

    :param xml_string: The XML string returned by the model.
    :return: A tuple of (final_answer_element, reasoning_element).
    """
    # Parse the XML string
    root = ET.fromstring(xml_string)

    # Find the 'final_answer' tag
    final_answer_element = root.find('final_answer')

    # Find the 'reasoning' tag
    reasoning_element = root.find('reasoning')

    return final_answer_element, reasoning_element


# GCP
def read_dimacs_format(dimacs_str):
    """Reads the DIMACS format string of a GCP instance.

    :param dimacs_str: The DIMACS format string of the GCP instance.
    :return: A tuple of (num_vertices, adjacency_list).
    """
    lines = dimacs_str.strip().split('\n')
    # Read the number of vertices and edges
    p_line = next(line for line in lines if line.startswith('p'))
    _, _, num_vertices, num_edges = p_line.split()
    num_vertices, num_edges = int(num_vertices), int(num_edges)

    # Create adjacency list
    adjacency_list = {i: set() for i in range(1, num_vertices + 1)}

    # Read the edges and ignore those that reference non-existing vertices
    for line in lines:
        if line.startswith('e'):
            _, vertex1, vertex2 = line.split()
            vertex1, vertex2 = int(vertex1), int(vertex2)
            if vertex1 in adjacency_list and vertex2 in adjacency_list:
                adjacency_list[vertex1].add(vertex2)
                adjacency_list[vertex2].add(vertex1)

    return num_vertices, adjacency_list


import ast
def parse_answer(llm_string):
    """Parses the answer string returned by the model.

    :param llm_string: The answer string returned by the model.
    :return: A dictionary of the answer.
    """
    all_answers, reasoning_element = parse_xml_to_dict(llm_string)
    all_answers = ast.literal_eval(all_answers.text)
    all_answers = {int(k):v for k,v in all_answers.items()}
    return all_answers #answer_dict


def gcpCheck(dimacs_str, answer_str):
    """Validates the solution for the GCP instance.

    :param dimacs_str: The DIMACS format string of the GCP instance.
    :param answer_str: The answer returned by the model.
    :return: A tuple of (is_correct, message).
    """
    num_vertices, adjacency_list = read_dimacs_format(dimacs_str)
    answer_colors = parse_answer(answer_str)
    # print(adjacency_list)
    # print(answer_colors)

    # Check if all colors in the answer are valid
    for vertex, neighbors in adjacency_list.items():
        for neighbor in neighbors:
            try:
                if answer_colors[vertex] == answer_colors[neighbor]:
                    print(f"Invalid coloring: Vertex {vertex} and {neighbor} have the same color.")
                    return False
            except:
                print(f"Invalid input.") # dealing with hullucination
                return False

    print(f"Valid coloring found with {len(set(answer_colors.values()))} colors: {answer_colors}")
    return True


# # Example usage:
# dimacs_format_str = """
# p edge 14 21
# e 1 2
# e 1 5
# e 2 3
# e 2 6
# e 3 4
# e 3 7
# e 4 8
# e 5 6
# e 5 9
# e 6 7
# e 6 10
# e 7 8
# e 7 11
# e 8 12
# e 9 10
# e 9 13
# e 10 11
# e 10 14
# e 11 12
# e 11 15
# e 12 16
# """
# answer_str = "{'Answer': ['1:A', '2:B', '3:C', '4:B', '5:C', '6:A', '7:C', '8:B', '9:A', '10:A', '11:B', '12:B', '13:C', '14:A']}"

# # Call the function with the example input
# gcpCheck(dimacs_format_str, answer_str)
