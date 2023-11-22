import ast

def read_dimacs_format(dimacs_str):
    lines = dimacs_str.strip().split('\n')
    p_line = next(line for line in lines if line.startswith('p'))
    _, _, num_vertices, num_edges = p_line.split()
    num_vertices, num_edges = int(num_vertices), int(num_edges)

    adjacency_list = {i: set() for i in range(1, num_vertices + 1)}
    for line in lines:
        if line.startswith('e'):
            _, vertex1, vertex2 = line.split()
            vertex1, vertex2 = int(vertex1), int(vertex2)
            if vertex1 in adjacency_list and vertex2 in adjacency_list:
                adjacency_list[vertex1].add(vertex2)
                adjacency_list[vertex2].add(vertex1)

    return num_vertices, adjacency_list

def parse_answer(answer_str):
    all_answers = ast.literal_eval(answer_str)['Answer']
    answer_dict = {}
    for pair in all_answers:
        vertex, color = pair.split(":")
        answer_dict[int(vertex)] = color
    return answer_dict

def gcp_decision_check(dimacs_str, answer_str, k_colors):
    num_vertices, adjacency_list = read_dimacs_format(dimacs_str)
    answer_colors = parse_answer(answer_str)

    # Check if the coloring uses no more than k_colors
    if len(set(answer_colors.values())) > k_colors:
        print(f"Invalid coloring: More than {k_colors} colors used.")
        return False

    # Check if adjacent vertices have different colors
    for vertex, neighbors in adjacency_list.items():
        for neighbor in neighbors:
            if answer_colors[vertex] == answer_colors[neighbor]:
                print(f"Invalid coloring: Vertex {vertex} and {neighbor} have the same color.")
                return False

    print("Valid coloring found.")
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
# k_colors = 3  # The target number of colors

# gcp_decision_check(dimacs_format_str, answer_str, k_colors)
