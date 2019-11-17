import curses
import random
from life import GameOfLife
from ui import UI
import time

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
        
        screen.addstr('Press spacebar to pause        Esc to exit')
        
        # Game is paused output PAUSED
        if self.isPaused == True:
            screen.addstr('\nPAUSED')
            

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        
        for row in range(self.life.rows):
            screen.addstr('│')
            for col in range(self.life.cols):
                # ⬤●•
                screen.addstr('⬤' if self.life.curr_generation[row][col] else '.')
            screen.addstr('│\n')
                
    def draw_life(self, screen, delay: int = 500) -> None:
        screen.clear()
        
        try:
            self.draw_borders(screen)
            self.draw_grid(screen)
            self.draw_borders(screen)
            self.draw_text(screen)
        except curses.error:
            raise ValueError("The window is too small for grid of this size")
        
        screen.refresh()
        curses.delay_output(delay)
            
    def run(self, delay: int = 500) -> None:
        screen = curses.initscr()
        
        # Key presses doesn't get typed
        curses.noecho()
        # Cursor visibility
        curses.curs_set(0)
        
        # Screen doesn't freeze waiting for input every time screen.getch() called
        screen.nodelay(True)
        
        while self.life.is_changing and not self.life.is_max_generations_exceed:
            
            self.draw_life(screen, delay)
            
            # Listen for spacebar keypress
            event = screen.getch()
            
            # If spacebar is pressed - PAUSE
            if event == 32:
                self.isPaused = True
                self.draw_life(screen, delay)
                while self.isPaused:
                    # Listen for spacebar keypress
                    if screen.getch() == 32:
                        self.isPaused = False
                # Reduce loop's CPU usage
                time.sleep(0.1)
            # If Esc is pressed - EXIT
            if event == 27:
                break
            # Next generation of life generated
            self.life.step()
            
                         
            
            
        curses.endwin()


if __name__ == '__main__':
    random.seed(1234)
    
    console = Console(GameOfLife((20, 120), True, 30))
    console.run()
