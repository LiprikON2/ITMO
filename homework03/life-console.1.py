import curses
import time
import argparse

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)
        self.isPaused = False

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        width = self.life.cols

        line = '+{}+\n'.format(('━' * width))
        screen.addstr(line)

    def draw_text(self, screen) -> None:
        """ Отображение текста """

        screen.addstr('[Press spacebar to pause]    [Esc to exit]')

        # Game is paused output PAUSED
        if self.isPaused:
            screen.addstr('\nPAUSED')

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """

        for row in range(self.life.rows):
            screen.addstr('│')
            for col in range(self.life.cols):
                # ⬤●•
                screen.addstr(
                    '⬤' if self.life.curr_generation[row][col] else '.')
            screen.addstr('│\n')

    def draw_life(self, screen, delay: int = 500) -> None:
        screen.clear()

        try:
            self.draw_borders(screen)
            self.draw_grid(screen)
            self.draw_borders(screen)
            self.draw_text(screen)

        except curses.error:
            raise ValueError(
                "The window is too small for the grid of this size")

        screen.refresh()
        curses.delay_output(delay)

    def run(self, delay: int = 500) -> None:
        screen = curses.initscr()

        # Key presses don't get typed
        curses.noecho()
        # Hide cursor
        curses.curs_set(0)

        # Screen doesn't freeze waiting for input every time screen.getch() called
        screen.nodelay(True)
        self.is_running = True

        while self.is_running and self.life.is_changing and not self.life.is_max_generations_exceed:

            self.draw_life(screen, delay)

            # Listen for keypresses
            event = screen.getch()

            # If spacebar is pressed - PAUSE
            if event == 32:
                self.isPaused = True
                self.draw_life(screen, delay)
                while self.isPaused:
                    # Listen for keypresses
                    event = screen.getch()

                    # Listen for spacebar keypress
                    if event == 32:
                        self.isPaused = False

                    # If Esc is pressed - EXIT
                    if event == 27:
                        self.isPaused = False
                        self.is_running = True

                # Reduce loop's CPU usage
                time.sleep(0.1)

            # If Esc is pressed - EXIT
            if event == 27:
                break

            # Next generation of life generated
            self.life.step()

        curses.endwin()


# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--rows", type=int, help="Amount of rows")
#     parser.add_argument("--cols", type=int, help="Amount of columns")
#     parser.add_argument("--max-generations", type=int,
#                         help="Maximum amount of generation")
#     args = parser.parse_args()
    
    
#     console = Console(GameOfLife((args.rows if args.rows else 6, args.cols if args.cols else 8), True, args.max_generations if args.max_generations else 10, 'grid.txt'))
#     console.run()


if __name__ == '__main__':
    console = Console(GameOfLife.from_file('grid.txt'))
    console.run()
