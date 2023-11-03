"""
Defines a generate_distance_matrix function to create a random symmetric matrix that represents the distances between nodes.
Includes a distance_matrix_to_csv function that takes a distance matrix and saves it to a CSV file.
Defines a generate_tsp_instances function that generates TSP instances for different levels of complexity based on the range of node counts.
Creates a folder named "Data" if it doesn't exist, where it will save the CSV files with the distance matrices.
"""

import numpy as np
import os
import pandas as pd

DATA_PATH = '../Data/'

# Create a directory for data if it doesn't exist
os.makedirs(DATA_PATH, exist_ok=True)

# Function to generate a random symmetric matrix to represent distances
def generate_distance_matrix(n, max_distance=100):
    # Create the upper triangle of the distance matrix with random values
    upper_triangle = np.random.randint(1, max_distance, size=(n, n))
    np.fill_diagonal(upper_triangle, 0)
    
    # Make the matrix symmetric
    distance_matrix = upper_triangle + upper_triangle.T - np.diag(upper_triangle.diagonal())
    
    return distance_matrix

# Save distance matrix to CSV format
def distance_matrix_to_csv(matrix, filename):
    df = pd.DataFrame(matrix)
    df.to_csv(filename, index=False, header=False)

# Generate instances of TSP
def generate_tsp_instances(node_ranges, num_instances_per_level):
    for level, node_range in enumerate(node_ranges):
        print(f"Generating instances for complexity level {level}")
        
        for instance_num in range(num_instances_per_level):
            n = np.random.choice(node_range)
            distance_matrix = generate_distance_matrix(n)
            filename = f"{DATA_PATH}synthesized_data_TSP_level_{level}_instance_{instance_num}.csv"
            distance_matrix_to_csv(distance_matrix, filename)

# Configuration for complexity levels
num_instances_per_level = 1 # will change to 100
node_ranges = [range(5, 11), range(10, 16), range(15, 21), range(20, 26), range(25, 31)]
generate_tsp_instances(node_ranges, num_instances_per_level)
