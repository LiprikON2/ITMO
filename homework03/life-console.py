import curses

from life import GameOfLife
from ui import UI

class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        # line = '+'.join(['-' * (life.width * 3)] * 3)
        # for row in range(life.width):
        #     for col in range(life.height):
        #         print(line)
        
        
        # width = 10
        # line = '+'.join(['-' * (width * 3)] * 3)
        # for row in range(9):
        #     print(''.join(grid[row][col].center(width) +
        #                 ('|' if str(col) in '25' else '') for col in range(9)))
        #     if str(row) in '25':
        #         print(line)

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        pass

    def run(self) -> None:
        screen = curses.initscr()
        # PUT YOUR CODE HERE
        curses.endwin()
