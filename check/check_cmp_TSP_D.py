import numpy as np
import pandas as pd
import networkx as nx


def tsp_approx(distance_matrix):
    """Returns an approximate solution to the TSP problem."""
    G = nx.from_numpy_array(distance_matrix)
    return nx.approximation.traveling_salesman_problem(G)

def tsp_decision_check(distance_matrix, threshold, tour):
    """
    Checks if a given TSP tour is valid and within the threshold distance.

    :param adj_matrix: Path to the CSV file containing the distance matrix and threshold.
    :param tour: String representing the TSP tour in the format "0->1->2->...->N->0"
    :return: Boolean indicating whether the tour is valid and within the threshold distance.
    """
    is_feasible = tour.get('Feasible', 'no').lower() == 'yes'

    # Calculate the approxed distance of the tour
    tours = tsp_approx(distance_matrix)
    tour_distance = sum(distance_matrix[tours[i], tours[i + 1]] for i in range(len(tours) - 1)) + \
                    distance_matrix[tours[-1], tours[0]]

    if is_feasible != (tour_distance <= threshold):
        return False, f"Feasibility mismatch: {is_feasible} vs {tour_distance} > {threshold}"
    return True, "Feasible: {} <= {}".format(tour_distance, threshold)



# # Example usage:

# # Path to the CSV file
# file_path = '../Data/TSP_Decision/decision_data_TSP_level_0_instance_1.csv'

# # Given a tour string (replace with your tour string)
# tour_string = {'Feasible': 'yes'}

# validity, message = tsp_decision_check(file_path, tour_string)
# print(message)
