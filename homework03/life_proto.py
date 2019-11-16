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
        # self.grid = self.create_grid(randomize=True)
        self.grid = [
            [1,1,0,0,1,1,1,1],
            [0,1,1,1,1,1,1,0],
            [1,0,1,1,0,0,0,0],
            [1,0,0,0,0,0,0,1],
            [1,0,1,1,1,1,0,0],
            [1,1,1,1,0,1,1,1]
        ]
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            
            # Отрисовка списка клеток
            self.draw_grid()
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.grid = self.get_next_generation()
            
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
            grid = [ [ random.choice([0, 1]) for i in range(self.cell_width) ] for j in range(self.cell_height) ]
        else: 
            grid = [ [ 0 for i in range(self.cell_width) ] for j in range(self.cell_height) ]
        
        return grid
        
    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        
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
        col, row = cell
        neighbours_arr = []
        
        # -┙ bottom right
        if (row + 1 < self.cell_width) and (col + 1 < self.cell_height):
            neighbours_arr.append(self.grid[col + 1][row + 1])
        # *| right
        if (row + 1 < self.cell_width):
            neighbours_arr.append(self.grid[col][row + 1])
            
        # ┍- top left
        if (row - 1 >= 0) and (col - 1 >= 0):
            neighbours_arr.append(self.grid[col - 1][row - 1])
        # |* left
        if (row - 1 >= 0):
            neighbours_arr.append(self.grid[col][row - 1])
            
        # -┐ top right
        if (row + 1 < self.cell_width) and (col - 1 >= 0):                
            neighbours_arr.append(self.grid[col - 1][row + 1])
        # ^^ top
        if (col - 1 >= 0):
            neighbours_arr.append(self.grid[col - 1][row])
            
        # └- bottom left
        if (row - 1 >= 0) and (col + 1 < self.cell_height):
            neighbours_arr.append(self.grid[col + 1][row - 1])
        # __ bottom
        if (col + 1 < self.cell_height):
            neighbours_arr.append(self.grid[col + 1][row])
        
        return neighbours_arr


    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.
        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        
        # Create empty grid
        next_grid = self.create_grid()
        
        for row in range(self.cell_width):
            for col in range(self.cell_height):
                neighbours_count = sum(self.get_neighbours((col, row)))
                
                # Determine if cell stays form previous grid
                if (neighbours_count >= 2) and (neighbours_count <= 3) and self.grid[col][row]:
                    next_grid[col][row] = 1
                # Determine if new cell appears
                elif neighbours_count == 3:
                    next_grid[col][row] = 1
                else: 
                    next_grid[col][row] = 0
        
        return next_grid
                    
                    

if __name__ == '__main__':
    game = GameOfLife(400, 300, 50, 0.25)
    game.run()