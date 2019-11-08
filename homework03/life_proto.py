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
            self.grid = [ [ random.choice([0, 1]) for i in range(self.cell_height) ] for j in range(self.cell_width) ]
        else: 
            self.grid = [ [ 0 for i in range(self.cell_height) ] for j in range(self.cell_width) ]
        
        return self.grid
        
    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for x in range(self.cell_width):
            for y in range(self.cell_height):
                if self.grid[x][y]:
                    pygame.draw.rect(self.screen, pygame.Color('Red'), 
                                     ((x * self.cell_size, y * self.cell_size), 
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
        x, y = cell
        Cells = []
        
        try:
            if self.grid[x + 1][y + 1]:
                Cells.append((x + 1, y + 1))
            if self.grid[x + 1][y]:
                Cells.append((x + 1, y))
            
            if self.grid[x - 1][y - 1]:
                Cells.append((x - 1, y - 1))
            if self.grid[x - 1][y]:
                Cells.append((x - 1, y))
                
            if self.grid[x + 1][y - 1]:                
                Cells.append((x + 1, y - 1))
            if self.grid[x][y - 1]:
                Cells.append((x, y - 1))
                
            if self.grid[x - 1][y + 1]:
                Cells.append((x - 1, y + 1))
            if self.grid[x][y + 1]:
                Cells.append((x, y + 1))
        except IndexError:
            pass
        
        return Cells

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        Grid = self.create_grid()
        for x in range(self.cell_width):
            for y in range(self.cell_height):
                neighbour_count = len(self.get_neighbours((x, y)))
                # Determine if cell stays
                if neighbour_count >= 2 and neighbour_count <= 3 and self.grid[x][y]:
                    Grid[x][y] = 1
                # Determine if cell appears
                if neighbour_count == 3:
                    Grid[x][y] = 1
        
        self.grid = Grid
                    
                    

if __name__ == '__main__':
    game = GameOfLife(320, 240, 40, 1)
    game.run()