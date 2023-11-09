# GCP
def read_dimacs_format(dimacs_str):
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
def parse_answer(answer_str):
    # # Convert the answer string to a dictionary
    # answer_dict = {}
    # # Remove the braces and split the string by commas
    # entries = answer_str.strip("}{").split(', ')
    # for entry in entries:
    #     vertex, color = entry.split(':')
    #     answer_dict[int(vertex)] = color
    # return answer_dict
    all_answers = ast.literal_eval(answer_str)['Answer']
    answer_dict = {}
    for pair in all_answers:
        vertex, color = pair.split(":")
        answer_dict[int(vertex)] = color
    return answer_dict


def gcpCheck(dimacs_str, answer_str):
    num_vertices, adjacency_list = read_dimacs_format(dimacs_str)
    answer_colors = parse_answer(answer_str)
    print(adjacency_list)
    print(answer_colors)

    # Check if all colors in the answer are valid
    for vertex, neighbors in adjacency_list.items():
        for neighbor in neighbors:
            if answer_colors[vertex] == answer_colors[neighbor]:
                print(f"Invalid coloring: Vertex {vertex} and {neighbor} have the same color.")
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



# MSP
def mspCheck(instance, solution):
    """
    Validate the MSP solution.

    Parameters:
    - instance: The MSP instance as a dictionary.
    - solution: A dictionary with meeting ids as keys and lists of scheduled time slots as values.

    Returns:
    - A tuple (is_valid, message). is_valid is True if the solution is valid, False otherwise.
      message contains information about the validity of the solution.
    """
    # convert solution to dictionary
    solution = ast.literal_eval(solution)["Answer"]
    # change string key to integer key
    solution = {int(k):v for k,v in solution.items()}

    # Check if all meetings are scheduled within the available time slots
    for meeting in instance['meetings']:
        m_id = meeting['id']
        duration = meeting['duration']
        scheduled_slots = solution.get(m_id, None)

        # Check if the meeting is scheduled
        if scheduled_slots is None:
            return False, f"Meeting {m_id} is not scheduled."

        # Check if the meeting fits within the number of total time slots
        if any(slot >= instance['time_slots'] for slot in scheduled_slots):
            return False, f"Meeting {m_id} does not fit within the available time slots."

        # Check if the scheduled slots are contiguous and fit the meeting duration
        if len(scheduled_slots) != duration or not all(
                scheduled_slots[i] + 1 == scheduled_slots[i + 1] for i in range(len(scheduled_slots) - 1)):
            return False, f"Meeting {m_id} is not scheduled in contiguous time slots fitting its duration."

        # Check if all participants are available at the scheduled time
        for p_id, participant in instance['participants'].items():
            if m_id in participant['meetings']:
                if not all(slot in participant['available_slots'] for slot in scheduled_slots):
                    return False, f"Participant {p_id} is not available for meeting {m_id} at the scheduled time."

    # Check if any participant is double-booked
    participants_schedule = {p_id: [] for p_id in instance['participants']}
    for m_id, time_slots in solution.items():
        duration = next(meeting['duration'] for meeting in instance['meetings'] if meeting['id'] == m_id)
        if len(time_slots) != duration:
            return False, f"Meeting {m_id} duration does not match the number of scheduled time slots."
        for p_id, participant in instance['participants'].items():
            if m_id in participant['meetings']:
                participants_schedule[p_id].extend(time_slots)

    for p_id, slots in participants_schedule.items():
        if len(slots) != len(set(slots)):
            return False, f"Participant {p_id} is double-booked."

    return True, "The solution is valid."

# Example usage:
# Define an example MSP instance
# Need to figure out how to deal with each timeslot's duration
msp_instance = {
    'meetings': [
        {'id': 0, 'duration': 2},
        {'id': 1, 'duration': 1}
    ],
    'participants': {
        0: {'available_slots': [0, 1, 2, 3], 'meetings': [0]},
        1: {'available_slots': [1, 2, 3, 4], 'meetings': [0, 1]}
    },
    'time_slots': 5,
    'complexity_level': 1
}

# Define a solution for the MSP instance
# meeting : list of slots
msp_solution = {
    0: [1,2],  # Meeting 0 scheduled at time slot 0
    1: [3]   # Meeting 1 scheduled at time slot 3
}

# # Validate the solution
# is_valid, message = mspCheck(msp_instance, msp_solution)
# print(is_valid, message)



# TSP
import numpy as np

def greedy_tsp(distance_matrix):
    """
    Solve the Traveling Salesman Problem using a greedy algorithm.

    :param distance_matrix: 2D numpy array where the element at [i, j] is the distance between city i and j
    :return: A tuple containing a list of the cities in the order they were visited and the total distance
    """
    num_cities = distance_matrix.shape[0]
    unvisited_cities = set(range(num_cities))
    current_city = np.random.choice(list(unvisited_cities))
    tour = [current_city]
    total_distance = 0

    while unvisited_cities:
        unvisited_cities.remove(current_city)
        if unvisited_cities:
            # Find the nearest unvisited city
            distances_to_unvisited = distance_matrix[current_city][list(unvisited_cities)]
            nearest_city = list(unvisited_cities)[np.argmin(distances_to_unvisited)]
            tour.append(nearest_city)
            # Update the total distance
            total_distance += distance_matrix[current_city, nearest_city]
            current_city = nearest_city

    # Return to start
    total_distance += distance_matrix[current_city, tour[0]]
    tour.append(tour[0])

    return tour, total_distance

# # Example usage:

# # Assuming distance_matrix is a 2D numpy array representing the distances
# # Replace this with your actual distance matrix
# distance_matrix = np.array([
#     [0, 2, 9, 10],
#     [1, 0, 6, 4],
#     [15, 7, 0, 8],
#     [6, 3, 12, 0]
# ])

# tour, total_distance = greedy_tsp(distance_matrix)
# print(f"The greedy TSP tour: {tour}")
# print(f"Total distance of the greedy TSP tour: {total_distance}")

def tspCheck(distance_matrix, tour_string):
    """
    Check if the TSP solution is complete and if the distance matches the greedy solution.
    
    :param tour_string: String representing the TSP tour in the format "0->1->2->...->N->0"
    :param distance_matrix: 2D numpy array representing the distances between cities
    :return: Boolean indicating whether the tour is complete and matches the greedy distance
    """
    # convert distance_matrix to numpy array
    distance_matrix = np.array(distance_matrix) 

    # Convert the tour string to a list of integers
    tour_string = ast.literal_eval(tour_string)['Answer']
    tour = list(map(int, tour_string.split('->')))
    
    # Check if tour is a cycle
    if tour[0] != tour[-1]:
        return False, "The tour must start and end at the same city."

    # Check if all cities are visited
    if len(tour) != len(distance_matrix) + 1:
        return False, "The tour does not visit all cities exactly once."

    # Calculate the distance of the provided tour
    tour_distance = sum(distance_matrix[tour[i]][tour[i + 1]] for i in range(len(tour) - 1))

    # Find the greedy tour distance for comparison
    greedy_tour, greedy_distance = greedy_tsp(distance_matrix)

    # Check if the provided tour distance is equal to the greedy tour distance
    if tour_distance != greedy_distance:
        return False, f"The tour distance ({tour_distance}) does not match the greedy solution ({greedy_distance})."
    
    return True, "The solution is complete and matches the greedy solution distance."

# Example usage:

# # Given a tour string (replace with your tour string)
# tour_string = "0->1->2->3->0"

# # Assuming distance_matrix is a previously defined numpy array representing the distances
# validity, message = tspCheck(tour_string, distance_matrix)
# print(message)

