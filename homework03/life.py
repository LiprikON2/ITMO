import pathlib
import random
import math
import os

from typing import List, Optional, Tuple


Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:

    def __init__(
        self,
        size: Tuple[int, int],
        randomize: bool = True,
        max_generations: Optional[float] = float('inf'),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()

        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)

        # Максимальное число поколений
        if max_generations:
            self.max_generations = max_generations

        # Текущее число поколений
        # FIXED from self.generations
        self.n_generation = 1

    def create_grid(self, randomize: bool = False) -> Grid:
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
            Матрица клеток размером `cols` х `rows`.
        """

        if randomize:
            grid = [[random.choice([0, 1]) for i in range(
                self.cols)] for j in range(self.rows)]
        else:
            grid = [[0 for i in range(self.cols)]
                    for j in range(self.rows)]

        return grid

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

        # -┙ bottom right border
        if (row + 1 < self.rows) and (col + 1 < self.cols):
            neighbours_arr.append(self.curr_generation[row + 1][col + 1])
        # *| right border
        if (row + 1 < self.rows):
            neighbours_arr.append(self.curr_generation[row + 1][col])

        # ┍- top left border
        if (row - 1 >= 0) and (col - 1 >= 0):
            neighbours_arr.append(self.curr_generation[row - 1][col - 1])
        # |* left border
        if (row - 1 >= 0):
            neighbours_arr.append(self.curr_generation[row - 1][col])

        # -┐ top right border
        if (row + 1 < self.rows) and (col - 1 >= 0):
            neighbours_arr.append(self.curr_generation[row + 1][col - 1])
        # ^^ top border
        if (col - 1 >= 0):
            neighbours_arr.append(self.curr_generation[row][col - 1])

        # └- bottom left border
        if (row - 1 >= 0) and (col + 1 < self.cols):
            neighbours_arr.append(self.curr_generation[row - 1][col + 1])
        # __ bottom border
        if (col + 1 < self.cols):
            neighbours_arr.append(self.curr_generation[row][col + 1])

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
        next_generation = self.create_grid()

        for row in range(self.rows):
            for col in range(self.cols):
                neighbours_count = sum(self.get_neighbours((row, col)))

                # Determine if cell stays form previous grid
                if (neighbours_count >= 2) and (neighbours_count <= 3) and self.curr_generation[row][col]:
                    next_generation[row][col] = 1
                # Determine if new cell appears
                elif neighbours_count == 3:
                    next_generation[row][col] = 1
                else:
                    next_generation[row][col] = 0

        return next_generation

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation.copy()
        self.curr_generation = self.get_next_generation()
        self.n_generation += 1

    @property
    # FIXED from is_max_generations_exceeded
    def is_max_generations_exceed(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations:
            return self.n_generation >= self.max_generations
        else:
            return False

    # Basically just a shortcut for creating readonly properties
    # is_changing = property(is_changing)
    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> 'GameOfLife':
        """
        Прочитать состояние клеток из указанного файла.
        """
        file = [c for c in open(filename).read() if c in '01\n']

        grid = [[]]  # type: List[List]
        j = 0
        # Split number rows into array of numbers, forming 2D matrix
        for i in range(len(file) - 1):
            if file[i] != '\n':
                number = [int(file[i])]
                grid[j].extend(number)
            else:
                grid.append([])
                j += 1
        rows = len(grid)
        cols = len(grid[0])
        life = GameOfLife((rows, cols))
        life.curr_generation = grid

        return life

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """

        file = open(filename, 'w+')
        for row in range(self.rows):
            for col in range(self.cols):
                number = str(self.curr_generation[row][col])
                file.write(number)
            file.write('\n')

        file.close()
