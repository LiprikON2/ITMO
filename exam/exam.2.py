# 1. Найти оптимальный путь
# 2. Найти оптимальный путь и не умереть
# 
# 👦 🌲 🏡 👹 👾 ⬜ ⬛

import random
from pprint import pprint as pp

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
    # print('Placed hero at', x,y)
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
    """ Converts grid to feed to pathfinding algorithm """
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

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:
        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)

# ref https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2

def find_closest_house(paths: list) -> list:
    """ From paths to different houses it retuns the shortest"""
    path_lengths = list(map(len, paths))
    index = path_lengths.index(min(path_lengths))
    
    return paths[index]

if __name__ == '__main__':
    
    # Ensure 🏡 is in generated grid
    iteration = 0
    while iteration < 100:
        grid = generate_grid(5)
        grid = place_hero_in_grid(grid)
        
        # grid = [['⬛', '👦', '⬛', '🌲', '⬛'], ['⬛', '🏡', '⬛', '🏡', '⬛'], ['⬛', '⬛', '🌲', '⬛', '👹'], ['⬛', '🌲', '🌲', '👹', '⬛'], ['👹', '⬛', '👾', '👾', '⬛']]
        if find_in_grid(grid, '🏡'):
            break
        iteration += 1

    render_grid(grid)
    converted_grid = convert_grid(grid)
    pp(converted_grid)
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
        print('start, end points:', start, end)
        n += 1
        paths.append(astar(converted_grid, start, end))
    
    final_path = find_closest_house(paths)
    print(final_path)
    print(paths, '\n\n\n')