import heapq

# generate answer for single source shortest path question
def answer_generate_SPP(q, start_node, end_node):
    edges = q['edges']

    print("We will use the dijkstra algorithm to solve this problem.")

    print("First, we need to initialize the distance array.")
    n = len(q['nodes'])
    print(f"The number of nodes in the graph is {n}")
    print("We will construct the adjacency matrix by iterating through the edges.")
    adj = [[float('inf')] * n for _ in range(n)]
    for edge in edges:
        print(f"Adding edge from {edge['from']} to {edge['to']} with weight {edge['weight']} to the adjacency matrix.")
        print(f"Adding edge from {edge['to']} to {edge['from']} with weight {edge['weight']} to the adjacency matrix.")
        adj[edge['from']][edge['to']] = edge['weight']
        adj[edge['to']][edge['from']] = edge['weight']
    print("For the unconnected nodes, we will set the distance to infinity.")
    print("The adjacency matrix is now as follows:")
    print(adj)

    print("We will start by setting the distance of the start node to 0 and all other nodes to infinity.")
    print(f"The distance array will be updated as we find the shortest path from start node {start_node} to all other nodes.")
    print("The distance array is initialized as follows:")
    distance = [float('inf')] * n
    print(f"We will set the distance of the start node {start_node} to 0.")
    distance[start_node] = 0
    print(f"The initial distance array is {distance}.")

    print("We will also initialize the visited array to keep track of the nodes we have visited.")
    print("visited = [False, False, False, False, ...]")
    visited = [False] * n

    print("We will use a priority queue of tuples to keep track of the nodes with the minimum distance.")
    print("The first element of the tuple will be the distance and the second element will be the node.")
    print("The priority queue is initialized as follows:")
    print("pq = [(0, start_node)]")
    pq = [(0, start_node)]

    print("We will now start the dijkstra algorithm.")
    print("While the priority queue is not empty, we will pop the node with the minimum distance.")
    print("We will then update the distance of its neighbors if the new distance is smaller.")
    print("We will also mark the node as visited.")
    print("We will continue this process until we have visited all the nodes or until we have found the shortest path to the end node.")

    print("The final distance array will contain the shortest distance from the start node to all other nodes.")
    print("We will return the distance of the end node as the shortest path from the start node to the end node.")

    print("Let's start the dijkstra algorithm.")
    while pq:
        print(f"The current priority queue is not empty: {pq}.")
        d, node = heapq.heappop(pq)
        print(f"Pop the node with the minimum distance: {node} with distance {d}.")
        if node == end_node:
            print(f"The popped node {node} is the end node {end_node}, so we have found the shortest path from {start_node} to {end_node} because we marked node {end_node} as visited.")
            break
        print(f"Pop node {node} with distance {d} because it has the minimum distance.")
        if visited[node]:
            print(f"Node {node} has already been visited. Skipping...")
            continue
        visited[node] = True
        print(f"Mark node {node} as visited as it hasn't been visited yet.")
        print(f"We will iterate through its neighbors and update their distances if necessary.")
        for neighbor, weight in enumerate(adj[node]):
            if weight != float('inf') and not visited[neighbor]:
                print(f"{neighbor} is a neighbor of {node} with the edge weight {weight}.")
                new_distance = d + weight
                print(f"One possible new distance from {start_node} to {neighbor} is {d} + {weight} = {new_distance}.")
                if new_distance < distance[neighbor]:
                    print(f"The new distance {new_distance} is smaller than the current distance {distance[neighbor]} from {start_node} to {neighbor}.")
                    distance[neighbor] = new_distance
                    heapq.heappush(pq, (new_distance, neighbor))
                else:
                    print(f"The new distance {new_distance} is not smaller than the current distance {distance[neighbor]} from {start_node} to {neighbor}.")
        print(f"The updated distance array is {distance}.")
        print(f"The updated priority queue is {pq}.")
    
    if distance[end_node] == float('inf'):
        print(f"There is no path from {start_node} to {end_node}.")
    else:
        print(f"The final distance array is {distance}.")
        print(f"Therefore, the shortest distance from {start_node} to {end_node} is {distance[end_node]}.")
    return distance[end_node] if distance[end_node] != float('inf') else "inf"


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
# spp_solution = {
#     'Path': "0->1->2->3",
#     'TotalDistance': 8
# }

# # Validate the solution
# answer_generate_SPP(spp_instance, start_node=1, end_node=2)