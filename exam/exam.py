# 1. Найти оптимальный путь
# 2. Найти оптимальный путь и не умереть
# 
# 👦 🌲 🏡 👹 👾 ⬜ ⬛

import random
from pprint import pprint as pp

def generate_grid(dims: int, symbols: list = None) -> list:
    if symbols is None: 
        symbols = ["⬛", "⬛", "⬛", "⬛", "⬛", "⬛", "🌲", "🌲", "🏡", "👹", "👾"]
    
    grid = [[random.choice(symbols) for dim in range(dims)] for dim in range(dims)]
    return grid

def find_in_grid(grid: list, symbol: str, index_of_symbol: int = 1) -> tuple:
    for y, line in enumerate(grid):
        for x, cell in enumerate(line):
            if cell == symbol and index_of_symbol == 1:
                return (x, y)
            elif cell == symbol:
                index_of_symbol -= 1

def place_hero_in_grid(grid: list) -> list:
    dims = len(grid)
    x = random.randint(0, dims - 1)
    y = random.randint(0, dims - 1)
    print('Placed hero at', x,y)
    grid[y][x] = '👦'
    return grid


def render_grid(grid: list) -> None:
    dims = len(grid)
    border1 = '┏' + ''.join(['━' for dim in range(2*dims)]) + '━┓'
    border2 = '┗' + ''.join(['━' for dim in range(2*dims)]) + '━┛'
    
    
    print(border1)
    for line in grid:
        print('┃' + ''.join(map(str, line)) + '┃' + '\n')
    print(border2)
    # print(border1 + middle + border2)
    # pp(grid)
    
def find_shortest_path(grid: list, point_a: tuple, point_b: tuple):
    dims = len(grid)


def get_neighbours(grid: list, pos: tuple) -> list:
    
    dims = len(grid)
    
    col, row = pos
    neighbours_arr = []

    # -┙ bottom right border
    if (row + 1 < dims) and (col + 1 < dims):
        neighbours_arr.append(grid[row + 1][col + 1])
    # *| right border
    if (row + 1 < dims):
        neighbours_arr.append(grid[row + 1][col])

    # ┍- top left border
    if (row - 1 >= 0) and (col - 1 >= 0):
        neighbours_arr.append(grid[row - 1][col - 1])
    # |* left border
    if (row - 1 >= 0):
        neighbours_arr.append(grid[row - 1][col])

    # -┐ top right border
    if (row + 1 < dims) and (col - 1 >= 0):
        neighbours_arr.append(grid[row + 1][col - 1])
    # ^^ top border
    if (col - 1 >= 0):
        neighbours_arr.append(grid[row][col - 1])

    # └- bottom left border
    if (row - 1 >= 0) and (col + 1 < dims):
        neighbours_arr.append(grid[row - 1][col + 1])
    # __ bottom border
    if (col + 1 < dims):
        neighbours_arr.append(grid[row][col + 1])

    return neighbours_arr



if __name__ == '__main__':
    
    # Ensure 🏡 is in generated grid
    iteration = 0
    while iteration < 100:
        grid = generate_grid(5)
        grid = place_hero_in_grid(grid)
        if find_in_grid(grid, '🏡'):
            break
        iteration += 1
        print('Trying again')
        
    
    s = find_in_grid(grid, '👦')
    b = get_neighbours(grid, s)
    print(b)
    
    
    render_grid(grid)
    
    # n = 1
    # while find_in_grid(grid, '🏡', n):
    #     s = find_in_grid(grid, '🏡', n)
    #     n += 1
    #     print(s)
        
    