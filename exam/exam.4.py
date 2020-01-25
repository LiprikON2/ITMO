# 1. Найти оптимальный путь
# 2. Найти оптимальный путь и не умереть
# 
# 👦 🌲 🏡 👹 👾 ⬛

import random
from pprint import pprint as pp
import heapq

health = 10

def generate_grid(dims: int, symbols: list = None) -> list:
    """ Generates 2d grid """
    if symbols is None: 
        symbols = ["⬛", "⬛", "⬛", "⬛", "⬛", "⬛", "🌲", "🌲", "🏡", "👹", "👾"]
    
    grid = [[random.choice(symbols) for dim in range(dims)] for dim in range(dims)]
    return grid


def find_in_grid(grid: list, symbol: str, index_of_symbol: int = 1) -> tuple:
    """ Finds specifed symbol in grid """
    for y, line in enumerate(grid):
        for x, cell in enumerate(line):
            if cell == symbol and index_of_symbol == 1:
                return (x, y)
            elif cell == symbol:
                index_of_symbol -= 1

def place_hero_in_grid(grid: list, symbol: str = '👦') -> list:
    """ Places symbol at random place in the grid"""
    dims = len(grid)
    x = random.randint(0, dims - 1)
    y = random.randint(0, dims - 1)
    grid[y][x] = symbol
    return grid


def render_grid(grid: list) -> None:
    """ Shows 2d grid in fancy manner """
    dims = len(grid)
    border1 = '┏' + ''.join(['━' for dim in range(2*dims)]) + '━┓'
    border2 = '┗' + ''.join(['━' for dim in range(2*dims)]) + '━┛'
    
    
    print(border1)
    for line in grid:
        print('┃' + ''.join(map(str, line)) + '┃' + '\n')
    print(border2)

def convert_grid(grid: list) -> list:
    """ Converts grid to feed it to the pathfinding algorithm """
    dims = len(grid)
    converted_grid = [['' for dim in range(dims)] for dim in range(dims)]
    for y, line in enumerate(grid):
        for x, cell in enumerate(line):
            if cell in ['🏡', '👦', '👹', '👾', '⬛']:
                converted_grid[y][x] = 0
            else:
                converted_grid[y][x] = 1
    # print(grid)
    return converted_grid

class Node:
    """
    A node class for A* Pathfinding
    """

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position
    
    def __repr__(self):
      return f"{self.position} - g: {self.g} h: {self.h} f: {self.f}"

    # defining less than for purposes of heap queue
    def __lt__(self, other):
      return self.f < other.f
    
    # defining greater than for purposes of heap queue
    def __gt__(self, other):
      return self.f > other.f

def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]  # Return reversed path


def astar(maze, start, end, grid, allow_diagonal_movement = False):
    """
    Returns a list of tuples as a path from the given start to the given end in the given maze
    :param maze:
    :param start:
    :param end:
    :return:
    """
    global health
    health = 10

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Heapify the open_list and Add the start node
    heapq.heapify(open_list) 
    heapq.heappush(open_list, start_node)

    # Adding a stop condition
    outer_iterations = 0
    max_iterations = (len(maze[0]) * len(maze) // 2)

    # what squares do we search
    adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0),)
    if allow_diagonal_movement:
        adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1),)

    # Loop until you find the end
    while len(open_list) > 0:
        outer_iterations += 1

        if outer_iterations > max_iterations:
          # if we hit this point return the path such as it is
          # it will not contain the destination
          print("giving up on pathfinding too many iterations")
          return None   
        
        # Get the current node
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            return return_path(current_node)

        # Generate children
        children = []
        
        for new_position in adjacent_squares: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue
            
            # Add monster support 
            if grid[node_position[0]][node_position[1]] in ['👹', '👾']:
                if grid[node_position[0]][node_position[1]] == '👾' and (health - 5 > 0):
                    health -= 5
                elif grid[node_position[0]][node_position[1]] == '👹' and (health - 10 > 0):
                    health -= 10
                else:
                    continue
                
            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            # Child is on the closed list
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            if len([open_node for open_node in open_list if child.position == open_node.position and child.g > open_node.g]) > 0:
                continue

            # Add the child to the open list
            heapq.heappush(open_list, child)

    print("Couldn't get a path to destination")
    return None

# ref https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
# Fixed verison https://gist.github.com/ryancollingwood/32446307e976a11a1185a5394d6657bc

def find_closest_house(paths: list) -> list:
    """ From paths to different houses it retuns the shortest"""
    # Remove None from the list
    paths = [path for path in paths if path is not None]
    path_lengths = list(map(len, paths))
    index = path_lengths.index(min(path_lengths))
    
    return paths[index]

if __name__ == '__main__':
    
    # Ensure 🏡 is in generated grid
    iteration = 0
    while iteration < 100:
        grid = generate_grid(5)
        grid = place_hero_in_grid(grid)
        
        if find_in_grid(grid, '🏡'):
            break
        iteration += 1

    render_grid(grid)
    maze = convert_grid(grid)
    pp(maze)
    
    # Start point of pathfinding
    start = find_in_grid(grid, '👦')
    n = 1
    paths = []
    while n < 100:
        # Pathfind for each house in the grid
        if find_in_grid(grid, '🏡', n) == None:
            break
        # End point of pathfinding
        end = find_in_grid(grid, '🏡', n)
        n += 1
        paths.append(astar(maze, start, end, grid))
    
    # print(paths, '\n\n\n')
    
    # Ensure path is found
    if paths[0]:
        final_path = find_closest_house(paths)
        print(final_path)
        
    print('remaining health:', health)