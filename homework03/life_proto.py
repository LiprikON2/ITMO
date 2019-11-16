import pygame
import random

from pygame.locals import *
from typing import List, Tuple


Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:

    def __init__(self, width: int=640, height: int=480, cell_size: int=10, speed: int=10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Создание списка клеток
        self.create_grid(randomize=True)
        
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    
                    
            # Отрисовка списка клеток
            self.draw_grid()
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.get_next_generation()
            
            
            
            self.draw_lines()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool=False) -> Grid:
        """
        Создание списка клеток.
        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.
        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.
        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        
        if randomize:
            self.grid = [ [ random.choice([0, 1]) for i in range(self.cell_width) ] for j in range(self.cell_height) ]
        else: 
            self.grid = [ [ 0 for i in range(self.cell_width) ] for j in range(self.cell_height) ]
        print("unaltered grid: ", self.grid)
        
        # TEMPORARY
        self.grid = [[1, 0, 0, 0], [0, 1, 1, 1], [0, 1, 1, 1], [1, 0, 1, 0]]
        return self.grid
        
    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        
        # print('IM DRAWING', self.grid)
        for row in range(self.cell_width):
            for col in range(self.cell_height):
                if self.grid[col][row]:
                    pygame.draw.rect(self.screen, pygame.Color('Red'), 
                                     ((row * self.cell_size, col * self.cell_size), 
                                      (self.cell_size, self.cell_size)))
                else: 
                    pygame.draw.rect(self.screen, pygame.Color('White'), 
                                     ((row * self.cell_size, col * self.cell_size), 
                                      (self.cell_size, self.cell_size)))
                    
                    
    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.
        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.
        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.
        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        row, col = cell
        neighbours_arr = []
        
        try:
            # -┙
            if (row + 1 < self.cell_width) and (col + 1 < self.cell_height):
                neighbours_arr.append((row + 1, col + 1))
            # *|
            if (row + 1 < self.cell_width):
                neighbours_arr.append((row + 1, col))
                
            # ┍-
            if (row - 1 >= 0) and (col - 1 >= 0):
                neighbours_arr.append((row - 1, col - 1))
            # |* (-)
            if (row - 1 >= 0):
                neighbours_arr.append((row - 1, col))
                
            # -┐   
            if (row + 1 < self.cell_width) and (col - 1 >= 0):                
                neighbours_arr.append((row + 1, col - 1))
            # ^^
            if (col - 1 >= 0):
                neighbours_arr.append((row, col - 1))
                
            # └-
            if (row - 1 >= 0) and (col + 1 < self.cell_height):
                neighbours_arr.append((row - 1, col + 1))
            # __
            if (col + 1 < self.cell_height):
                neighbours_arr.append((row, col + 1))
        
        except IndexError:
            print('indexError')
            pass
        
        
                
        
        
        
        
        
        
        
        
        
        # x, y = cell
        # neighbours_arr = []
        
        # if x+1 > self.cell_width - 1:
        #     x_max = x
        # else:
        #     x_max = x+1
        # if y+1 > self.cell_height - 1:
        #     y_max = y
        # else:
        #     y_max = y+1
        
        # if x-1 < 0:
        #     x_min = x
        # else:
        #     x_min = x-1
        # if y-1 < 0:
        #     y_min = y
        # else:
        #     y_min = y-1
            
        #     # print('dimentions {}x{}'.format(self.cell_width, self.cell_height))
        #     # print("X Получилось минимум - {} макс - {}".format(x_min, x_max))
        #     # print("Y Получилось минимум - макс - {}".format(y_max))
            
        # try:
        #     for i in range(x_min, x_max+1):
        #         for j in range(y_min, y_max+1):
        #             if self.grid[i][j] and x != i and y != j:
        #                 neighbours_arr.append((i, j))
        #                 print("Sooo... x={} y={} but".format(x, y), range(x_min, x_max+1), range(y_min, y_max+1))
        # except IndexError:
        #     print("thats not supposed to happen")
            
        # print(self.grid)
        # range(-1, 1) is equal -1, 0
            
        # for i in range(4, 6+1): - 4, 5, 6
        #     print(i)
            
                    
        
        # return [(1, 1), (0, 1), (1, 0)]
        # try:
        #     if self.grid[x + 1][y + 1]:
        #         neighbours_arr.append((x + 1, y + 1))
        #     if self.grid[x + 1][y]:
        #         neighbours_arr.append((x + 1, y))
            
        #     if self.grid[x - 1][y - 1] and x + y > 2:
        #         neighbours_arr.append((x - 1, y - 1))
        #     if self.grid[x - 1][y] and x > 1:
        #         neighbours_arr.append((x - 1, y))
                
        #     if self.grid[x + 1][y - 1] and y > 1:                
        #         neighbours_arr.append((x + 1, y - 1))
        #     if self.grid[x][y - 1]  and y > 1:
        #         neighbours_arr.append((x, y - 1))
                
        #     if self.grid[x - 1][y + 1] and x > 1:
        #         neighbours_arr.append((x - 1, y + 1))
        #     if self.grid[x][y + 1]:
        #         neighbours_arr.append((x, y + 1))
        # except IndexError:
        #     pass
        
        return neighbours_arr

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.
        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        
        
        
        # Lets try again
        
        grid_copy = self.grid.copy()
        
        for row in range(self.cell_width):
            for col in range(self.cell_height):
                neighbour_count = 0
                neighbours_arr = self.get_neighbours((row, col))
                for i in range(len(neighbours_arr)):
                    neighbour_row, neighbour_col = neighbours_arr[i]
                    print('is row={} col={} == ? is it one? lets see'.format(neighbour_row, neighbour_col))
                    if self.grid[neighbour_col][neighbour_row]:
                        print("YES")
                        neighbour_count +=1
                    
                
                
                # print('A guy at {}, {} has {} neighbours:'.format(row, col, neighbour_count), neighbours_arr)

                
                # Determine if cell stays
                if (neighbour_count >= 2) and (neighbour_count <= 3) and self.grid[col][row]:
                    grid_copy[col][row] = 1
                # Determine if cell appears
                elif neighbour_count == 3:
                    grid_copy[col][row] = 1
                else: 
                    grid_copy[col][row] = 0
                
        # print('--------------------------------')
        # # print('here comes grid:', self.grid)
        # print('IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII')
                
        self.grid = grid_copy
        
                    
                    

if __name__ == '__main__':
    game = GameOfLife(160, 160, 40, 0.15)
    game.run()