import ast
import json

# KSP
def kspCheck(instance, solution):
    """
    Validate the KSP solution.

    Parameters:
    - instance: The KSP instance as a dictionary.
    - solution: A dictionary with item ids as keys and a boolean indicating if the item is selected.

    Returns:
    - A tuple (is_valid, message). is_valid is True if the solution is valid, False otherwise.
      message contains information about the validity of the solution.
    """
    # Convert solution to dictionary
    solution = ast.literal_eval(solution)["Answer"]
    # Change string key to integer key and value to boolean
    solution = {int(k): (v.lower() == 'true') for k, v in solution.items()}

    total_weight = 0
    total_value = 0

    # Calculate total weight and value of selected items
    for item in instance['items']:
        item_id = item['id']
        if solution.get(item_id, False):
            total_weight += item['weight']
            total_value += item['value']

            # Check if the item weight exceeds the knapsack capacity
            if total_weight > instance['knapsack_capacity']:
                return False, f"Total weight {total_weight} exceeds knapsack capacity {instance['knapsack_capacity']}."

    return True, f"The solution is valid with total weight {total_weight} and total value {total_value}."

# # Example usage:
# # Define an example KSP instance
# ksp_instance = {
#     'items': [
#         {'id': 0, 'weight': 10, 'value': 60},
#         {'id': 1, 'weight': 20, 'value': 100},
#         # ... add more items
#     ],
#     'knapsack_capacity': 50
# }

# # Define a solution for the KSP instance
# ksp_solution = {
#     0: 'true',  # Item 0 is selected
#     1: 'false'  # Item 1 is not selected
# }

# # Validate the solution
# is_valid, message = kspCheck(ksp_instance, json.dumps({'Answer': ksp_solution}))
# print(is_valid, message)
