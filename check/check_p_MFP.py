import ast
import json

# SPP - TODO: update this, this is completely wrong...
def mfp_check(instance, solution, start_node, end_node):
    """
    Validate the SPP solution.

    Parameters:
    - instance: The SPP instance as a dictionary with 'nodes' and 'edges'.
    - solution: A dictionary with 'path' as a list of nodes representing the path and 'total_cost' as the total cost of the path.
    - start_node: The starting node of the path.
    - end_node: The destination node of the path.

    Returns:
    - A tuple (is_valid, message). is_valid is True if the solution is valid, False otherwise.
      message contains information about the validity of the solution.
    """
    # Convert solution to dictionary
    solution = ast.literal_eval(solution)["Answer"]
    path = solution.get('path', [])
    total_cost = solution.get('total_cost', -1)

    # Check if path starts and ends with the correct nodes
    if not path or path[0] != start_node or path[-1] != end_node:
        return False, "The path does not start or end at the correct nodes."

    # Check if the path is continuous and calculate the cost
    calculated_cost = 0
    for i in range(len(path) - 1):
        from_node, to_node = path[i], path[i + 1]
        edge = next((edge for edge in instance['edges'] if edge['from'] == from_node and edge['to'] == to_node), None)

        if not edge:
            return False, f"No edge found from node {from_node} to node {to_node}."

        calculated_cost += edge['weight']

    # Check if the calculated cost matches the total cost provided in the solution
    if calculated_cost != total_cost:
        return False, f"The calculated cost ({calculated_cost}) does not match the provided total cost ({total_cost})."

    return True, "The solution is valid."

# # Example usage:
# # Define an example SPP instance
# spp_instance = {
#     'nodes': [0, 1, 2, 3],
#     'edges': [
#         {'from': 0, 'to': 1, 'weight': 4},
#         {'from': 1, 'to': 2, 'weight': 1},
#         {'from': 2, 'to': 3, 'weight': 3},
#         {'from': 0, 'to': 3, 'weight': 6}
#     ],
#     'complexity_level': 1
# }

# # Define a solution for the SPP instance
# spp_solution = json.dumps({
#     'Answer': {
#         'path': [0, 1, 2, 3],
#         'total_cost': 8
#     }
# })

# # Validate the solution
# is_valid, message = spp_check(spp_instance, spp_solution, start_node=0, end_node=3)
# print(is_valid, message)
