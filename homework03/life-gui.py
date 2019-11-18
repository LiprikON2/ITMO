import pygame
from pygame.locals import *
import time
import argparse
import pathlib


from life import GameOfLife
from ui import UI


class GUI(UI):

    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)

        # in px
        self.cell_size = cell_size

        # in px
        self.width = self.life.cols * self.cell_size
        self.height = self.life.rows * self.cell_size

        # in px
        self.screen_size = self.width, self.height

        self.screen = pygame.display.set_mode(self.screen_size)

        self.speed = speed

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """

        for col in range(self.life.cols):
            for row in range(self.life.rows):
                if self.life.curr_generation[row][col]:
                    pygame.draw.rect(self.screen, pygame.Color('Red'),
                                     ((col * self.cell_size, row * self.cell_size),
                                      (self.cell_size, self.cell_size)))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('White'),
                                     ((col * self.cell_size, row * self.cell_size),
                                      (self.cell_size, self.cell_size)))

    def pause(self) -> None:
        """ Постановка игры на паузу """

        is_paused = True
        self.draw_grid()
        # Change cursor style
        pygame.mouse.set_cursor(*pygame.cursors.tri_left)
        while is_paused:
            for event in pygame.event.get():
                # Quit
                if event.type == QUIT:
                    is_paused = False
                    self.is_running = False
                    break

                # Listen for spacebar keypress - RESUME
                if event.type == pygame.KEYDOWN and event.key == 32:
                    is_paused = False
                    # Change cursor back
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)
                # Listen for S keypress - SAVE
                if event.type == pygame.KEYDOWN and event.key == 115:
                    self.life.save(pathlib.Path('Save.txt'))

                # On mouse button press: if right click - HANDLE CLICK
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_click(event)

            # Reduce loop's CPU usage
            time.sleep(0.01)

    def handle_click(self, event):
        """ Преключение состояния выбраной клетки """

        x, y = event.pos
        target_row = y // self.cell_size
        target_col = x // self.cell_size

        self.life.curr_generation = self.life.prev_generation.copy()

        # kill cell
        if self.life.curr_generation[target_row][target_col]:
            self.life.curr_generation[target_row][target_col] = 0
        # or resurrect cell
        else:
            self.life.curr_generation[target_row][target_col] = 1

        self.draw_grid()
        self.draw_lines()
        pygame.display.flip()

    def run(self) -> None:
        """ Запустить игру """

        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life: [Pause: SPACE] [Save: S]')
        self.screen.fill(pygame.Color('white'))

        self.is_running = True
        # while running and self.life.is_changing and not self.life.is_max_generations_exceed:
        while self.is_running and not self.life.is_max_generations_exceed:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.is_running = False

                # Listen for spacebar keypress - PAUSE
                if event.type == pygame.KEYDOWN and event.key == 32:
                    self.pause()
                # Listen for S keypress - SAVE
                if event.type == pygame.KEYDOWN and event.key == 115:
                    self.life.save(pathlib.Path('Save.txt'))

            # Отрисовка списка клеток
            self.draw_grid()

            # Выполнение одного шага игры (обновление состояния ячеек)
            self.life.step()

            self.draw_lines()
            pygame.display.flip()

            # Pause the game if nothing is changing
            if not self.life.is_changing:
                self.pause()
            clock.tick(self.speed)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", type=int,
                        help="Width of a window in px. Default: 500")
    parser.add_argument("--height", type=int,
                        help="Height of a window in px. Default: 500")
    parser.add_argument("--cell_size", type=int,
                        help="Size of a single cell in px. Default: 20")
    parser.add_argument("--max-generations", type=int,
                        help="Maximum amount of generation. Default: 500")
    parser.add_argument("--speed", type=int,
                        help="Speed in pygame ticks. Default: 1")

    args = parser.parse_args()

    # Iterate over arguments to set defaults
    # https://stackoverflow.com/questions/4075190/what-is-getattr-exactly-and-how-do-i-use-it
    for arg in vars(args):
        if not getattr(args, arg) and (arg == 'width' or arg == 'height' or arg == 'max_generations'):
            # setattr(x, 'y', val) is equivalent to `x.y = val`
            setattr(args, arg, 500)
        elif not getattr(args, arg) and (arg == 'cell_size'):
            setattr(args, arg, 20)
        elif not getattr(args, arg):
            setattr(args, arg, 5)

    game = GUI(GameOfLife((args.height // args.cell_size, args.width //
                           args.cell_size), True, args.max_generations), args.cell_size, args.speed)
    game.run()


# Run from save file
# if __name__ == '__main__':
#     console = GUI(GameOfLife.from_file(pathlib.Path('Save.txt')))
#     console.run()
