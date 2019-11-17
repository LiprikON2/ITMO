import curses
import random
from life import GameOfLife
from ui import UI

class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)
        

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        width = self.life.rows
        
        line = '+{}+\n'.format(('-' * width))
        screen.addstr(line)
        

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        
        self.draw_borders(screen)
        for row in range(self.life.rows):
            screen.addstr('|')
            for col in range(self.life.cols):
                screen.addstr('*' if self.life.curr_generation[row][col] else ' ')
            screen.addstr('|\n')
            
            if row == self.life.cols - 1:
                self.draw_borders(screen)
                
        screen.refresh()

    def run(self) -> None:
        screen = curses.initscr()
        # PUT YOUR CODE HERE
        while self.life.is_changing and not self.life.is_max_generations_exceeded:
            self.draw_grid(screen)
            self.life.step()
            curses.delay_output(1000)
            screen.clear()
        curses.endwin()
        # screen.getkey()


if __name__ == '__main__':
    random.seed(1234)
    
    console = Console(GameOfLife((5, 5), True, 120))
    console.run()
