def bsp_check(instance, solution):
    # Check if the solution is valid
    array = sorted(instance['array'])
    target_value = instance['target']
    position = int(solution.get('Position', -1))
    if position == -1 or position >= len(array):
        return False, f"The solution is invalid."
    elif array[position] != target_value:
        return False, f"The target index is incorrect."
    return True, "The solution is valid."