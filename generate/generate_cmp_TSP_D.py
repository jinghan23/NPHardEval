import numpy as np
import os
import pandas as pd

DATA_PATH = '../Data/TSP_Decision/'

# Create a directory for data if it doesn't exist
os.makedirs(DATA_PATH, exist_ok=True)

def generate_distance_matrix(n, max_distance=100):
    upper_triangle = np.random.randint(1, max_distance, size=(n, n))
    np.fill_diagonal(upper_triangle, 0)
    distance_matrix = upper_triangle + upper_triangle.T - np.diag(upper_triangle.diagonal())
    return distance_matrix

def generate_threshold(distance_matrix, threshold_factor=0.75):
    total_distance = np.sum(distance_matrix) / 2  # as matrix is symmetric
    threshold = total_distance * threshold_factor
    return threshold

def distance_matrix_to_csv(matrix, threshold, filename):
    df = pd.DataFrame(matrix)
    df.loc[len(df)] = threshold  # Adding threshold as the last row
    df.to_csv(filename, index=False, header=False)

def generate_tsp_instances(node_nums, num_instances_per_level, threshold_factor):
    for level, node_num in enumerate(node_nums):
        for i in range(1, num_instances_per_level + 1):
            print(f"Generating instances for complexity level {level}, instance {i}")
            distance_matrix = generate_distance_matrix(node_num)
            threshold = generate_threshold(distance_matrix, threshold_factor)
            filename = f"{DATA_PATH}decision_data_TSP_level_{level}_instance_{i}.csv"
            distance_matrix_to_csv(distance_matrix, threshold, filename)

# Configuration for complexity levels
num_instances_per_level = 10
node_nums = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
threshold_factor = 0.75  # Example threshold factor
generate_tsp_instances(node_nums, num_instances_per_level, threshold_factor)
