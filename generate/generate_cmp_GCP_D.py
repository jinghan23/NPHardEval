import networkx as nx
import random
import os

DATA_PATH = '../Data/GCP-D/'

# Create a directory for data if it doesn't exist
os.makedirs(DATA_PATH, exist_ok=True)

# Function to generate a random graph
def generate_graph(n, p):
    return nx.erdos_renyi_graph(n, p)

# Function to generate questions
def generate_questions(num_levels=10, questions_per_level=10):
    for level in range(1, num_levels + 1):
        for question in range(1, questions_per_level + 1):
            n = random.randint(level * 2, level * 3)  # Increasing the number of vertices with level
            p = random.uniform(0.3, 0.6)  # Edge probability
            g = generate_graph(n, p)

            # Number of colors for the question, inversely proportional to the level of difficulty
            num_colors = max(3, int((num_levels - level) / num_levels * n / 2))

            # Save the graph and the question
            nx.write_adjlist(g, f"{DATA_PATH}graph_level_{level}_q_{question}.adjlist")
            with open(f"{DATA_PATH}question_level_{level}_q_{question}.txt", "w") as file:
                file.write(f"Can the graph be colored with {num_colors} colors without any adjacent vertices having the same color?")

generate_questions()
