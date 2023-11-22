import numpy as np
import pandas as pd
import ast

def read_distance_matrix_and_threshold(file_path):
    """
    Reads the distance matrix and the threshold distance from the CSV file.

    :param file_path: Path to the CSV file containing the distance matrix and threshold.
    :return: A tuple containing the distance matrix as a numpy array and the threshold distance.
    """
    df = pd.read_csv(file_path, header=None)
    threshold = df.iloc[-1, 0]  # Last row contains the threshold
    distance_matrix = df.iloc[:-1].to_numpy()
    return distance_matrix, threshold

def tsp_decision_check(file_path, tour_string):
    """
    Checks if a given TSP tour is valid and within the threshold distance.

    :param file_path: Path to the CSV file containing the distance matrix and threshold.
    :param tour_string: String representing the TSP tour in the format "0->1->2->...->N->0"
    :return: Boolean indicating whether the tour is valid and within the threshold distance.
    """
    distance_matrix, threshold = read_distance_matrix_and_threshold(file_path)
    tour = list(map(int, tour_string.split('->')))

    # Check if tour is a cycle and visits all cities
    if tour[0] != tour[-1] or len(set(tour[:-1])) != len(distance_matrix):
        return False, "The tour must start and end at the same city and visit all cities exactly once."

    # Calculate the distance of the tour
    tour_distance = sum(distance_matrix[tour[i]][tour[i + 1]] for i in range(len(tour) - 1))

    # Check if the tour distance is within the threshold
    if tour_distance <= threshold:
        return True, f"The tour is valid and within the threshold (Tour distance: {tour_distance}, Threshold: {threshold})."
    else:
        return False, f"The tour exceeds the threshold (Tour distance: {tour_distance}, Threshold: {threshold})."

# Example usage:

# # Path to the CSV file
# file_path = 'path/to/your/csvfile.csv'

# # Given a tour string (replace with your tour string)
# tour_string = "0->1->2->3->0"

# validity, message = tsp_decision_check(file_path, tour_string)
# print(message)
