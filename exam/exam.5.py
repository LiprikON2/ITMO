# 1. Найти оптимальный путь
# 2. Найти оптимальный путь и не умереть
# 
# 👦 🌲 🏡 👹 👾 ⬛

import random
from pprint import pprint as pp
import heapq
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

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
    start_x, start_y = find_in_grid(grid, '👦')
    n = 1
    paths = []
    while n < 100:
        # Pathfind for each house in the grid
        if find_in_grid(grid, '🏡', n) == None:
            break
        # End point of pathfinding
        end_x, end_y = find_in_grid(grid, '🏡', n)
        n += 1
        path_maze = Grid(matrix=maze)
        
        start = grid.node(start_x, start_y)
        end = grid.node(end_x, end_y)
        finder = AStarFinder()
        path, runs = finder.find_path(start, end, path_maze)
        paths.append(path)
    
    # print(paths, '\n\n\n')
    
    # Ensure path is found
    if paths[0]:
        final_path = find_closest_house(paths)
        print(final_path)
        
    print('remaining health:', health)
    
# Not complete
# ref: https://pypi.org/project/pathfinding/