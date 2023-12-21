import frigidum
import random

def parse_graph(file_content):
    """
    Parses the content of a graph file into an adjacency matrix.

    Args:
        file_content (str): The content of the file as a string.

    Returns:
        list: An adjacency matrix representing the graph.
    """
    lines = file_content.split('\n')
    edges = []
    num_vertices = 0
    num_edges = 0

    for line in lines:
        if line.startswith('c'):
            continue  # Skip comment lines
        elif line.startswith('p'):
            parts = line.split()
            num_vertices = int(parts[2])
            num_edges = int(parts[3])
        elif line.startswith('e'):
            parts = line.split()
            edge = (int(parts[1]), int(parts[2]))
            edges.append(edge)

    # Create an adjacency matrix to represent the graph
    adjacency_matrix = [[0 for _ in range(num_vertices)] for _ in range(num_vertices)]
    
    for edge in edges:
        adjacency_matrix[edge[0] - 1][edge[1] - 1] = 1
        adjacency_matrix[edge[1] - 1][edge[0] - 1] = 1

    return adjacency_matrix


adjacency_matrix = None

# Reading the file and parsing its content
file_path = 'fpsol2.i.1.col'  # Replace with the correct file path if needed
with open(file_path, 'r') as file:
    file_content = file.read()
    adjacency_matrix = parse_graph(file_content)

# Now 'adjacency_matrix' contains the graph representation
# You can use 'adjacency_matrix' for further processing or analysis


def create_initial_solution(num_vertices):
    """
    Creates an initial solution for the graph coloring problem where each vertex is colored uniquely.

    Args:
        num_vertices (int): The number of vertices in the graph.

    Returns:
        list: A list representing the initial color of each vertex.
    """
    # Each vertex is colored with its own number (adjusted for zero-based indexing)
    return [i for i in range(num_vertices)]


def verify_solution(adjacency_matrix, solution):
    """
    Verifies if a given coloring solution is valid (no adjacent vertices share the same color).

    Args:
        adjacency_matrix (list): The adjacency matrix of the graph.
        solution (list): The coloring solution to verify.

    Returns:
        bool: True if the solution is valid, False otherwise.
    """
    num_vertices = len(adjacency_matrix)

    for i in range(num_vertices):
        for j in range(num_vertices):
            if adjacency_matrix[i][j] == 1:  # If vertices i and j are connected
                if solution[i] == solution[j]:  # Check if they have the same color
                    return False  # Adjacent vertices have the same color, not a valid solution
    return True  # All adjacent vertices have different colors, valid solution


def free_colors_for_vertex(vertex, adjacency_matrix, solution):
    """
    Determines the available colors that can be assigned to a specified vertex.

    Args:
        vertex (int): The vertex to check for available colors.
        adjacency_matrix (list): The adjacency matrix of the graph.
        solution (list): The current coloring solution.

    Returns:
        list: A list of available colors for the vertex.
    """
    num_vertices = len(adjacency_matrix)
    max_color = max(solution)
    used_colors = set()

    # Find colors used by adjacent vertices
    for i in range(num_vertices):
        if adjacency_matrix[vertex][i] == 1:
            used_colors.add(solution[i])

    # Find available colors
    available_colors = [color for color in range(max_color + 1) if color not in used_colors]

    return available_colors

# # Example usage
# vertex = 0 
# available_colors = free_colors_for_vertex(vertex, adjacency_matrix, initial_solution)
# print("Available colors for vertex", vertex, ":", available_colors)


def recolor_vertex(adjacency_matrix, solution):
    """
    Randomly selects a vertex and recolors it with an available color.

    Args:
        adjacency_matrix (list): The adjacency matrix of the graph.
        solution (list): The current coloring solution.

    Returns:
        list: A new coloring solution with one vertex recolored.
    """
    num_vertices = len(adjacency_matrix)
    new_solution = solution.copy()

    # Step 1: Select a random vertex
    vertex_to_recolor = random.randint(0, num_vertices - 1)

    # Step 2: Find available colors for this vertex
    available_colors = free_colors_for_vertex(vertex_to_recolor, adjacency_matrix, solution)

    # Step 3: Choose a new color, excluding the current color
    current_color = solution[vertex_to_recolor]
    available_colors = [color for color in available_colors if color != current_color]

    if available_colors:  # Ensure there is at least one available color
        new_color = random.choice(available_colors)
        # Step 4: Recolor the vertex
        new_solution[vertex_to_recolor] = new_color

    # Step 5: Return the updated solution
    return new_solution


def objective_colors_used(solution):
    """
    Calculates the number of unique colors used in a coloring solution.

    Args:
        solution (list): The coloring solution.

    Returns:
        int: The number of unique colors used.
    """
    # Count the unique colors in the solution
    unique_colors = set(solution)
    return len(unique_colors)

def objective_color_class_square_sum(solution):
    """
    Calculates the negative sum of the squares of the sizes of color classes in the solution. 
    This objective function is used to encourage a more balanced distribution of colors 
    across vertices in the graph coloring problem.

    Each color class is defined by the vertices colored with the same color. The size of 
    a color class is the number of vertices with that color. This function squares the size 
    of each color class and sums these values across all classes. The negative of this sum 
    is returned as the objective value.

    Args:
        solution (list): The coloring solution, where each element in the list represents 
                         the color of the corresponding vertex in the graph.

    Returns:
        int: The negative sum of the squares of the sizes of the color classes. A lower 
             value (more negative) indicates a more balanced color distribution.
    """
    color_class_sizes = {}
    
    # Count the number of vertices for each color
    for color in solution:
        if color in color_class_sizes:
            color_class_sizes[color] += 1
        else:
            color_class_sizes[color] = 1

    # Sum the squares of the color class sizes
    sum_of_squares = sum(size ** 2 for size in color_class_sizes.values())
    return -1 * sum_of_squares



# Assuming adjacency_matrix is already defined
# Define the functions needed for SA

def initial_solution():
    return create_initial_solution(len(adjacency_matrix))

def recolor_one_vertex(solution):
    """
    Function to be used as a neighbor function in simulated annealing, 
    which recolors one vertex in the solution.

    Args:
        solution (list): The current coloring solution.

    Returns:
        list: A new coloring solution with one vertex recolored.
    """
    return recolor_vertex(adjacency_matrix, solution)

def objective_gcp(solution):
    return objective_colors_used(solution)

# Simulated Annealing process
local_opt = frigidum.sa(
    random_start=initial_solution, 
    neighbours=[recolor_one_vertex], 
    objective_function=objective_gcp, 
    T_start=10**4, 
    T_stop=0.5, 
    repeats=10**2, 
    copy_state=frigidum.annealing.copy
)

# The result
print("Optimized solution:", local_opt)
print("Colors Used solution:", objective_colors_used(local_opt[0]))

valid_solution = verify_solution(adjacency_matrix, local_opt[0] )
print(f"Solution Valid?: {valid_solution}")
