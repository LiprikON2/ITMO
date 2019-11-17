import pygame
from pygame.locals import *
import random
import time

from life import GameOfLife
from ui import UI


class GUI(UI):

    def __init__(self, life: GameOfLife, cell_size: int=10, speed: int=10) -> None:
        super().__init__(life)
        
        self.cell_size = cell_size
        
        # px
        self.width = self.life.cols * self.cell_size
        self.height = self.life.rows * self.cell_size
        
        self.screen_size = self.width, self.height
        
        self.screen = pygame.display.set_mode(self.screen_size)
        
        self.speed = speed
        
        self.isPaused = False

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
        self.isPaused = True
        while self.isPaused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == 32:
                    self.isPaused = False
                        
                # On mouse button press: if right click - HANDLE CLICK
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_click(event)
            time.sleep(0.01)
            
    def handle_click(self, event):
        x, y = event.pos
        target_row = y // self.cell_size
        target_col = x // self.cell_size
        
        # get clicked cell
        target = self.life.prev_generation[target_row][target_col]
        print(target)
        # kill it
        if target:
            target = 0
        # or resurrect it
        else:
            target = 1
            
        target = self.life.curr_generation
        
        self.draw_grid()
        self.draw_lines()
        
        pygame.display.flip()
            
        print('Tar row:', target_row, "Tar col:", target_col)
                        
    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        
        running = True
        while running and self.life.is_changing and not self.life.is_max_generations_exceed:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    
                # On keydown: if spacebar is pressed - PAUSE
                if event.type == pygame.KEYDOWN and event.key == 32:
                    self.pause()
            # Отрисовка списка клеток
            self.draw_grid()
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.life.step()
            
            self.draw_lines()
            pygame.display.flip()
            
            
                        
                
            clock.tick(self.speed)
                    
        pygame.quit()

if __name__ == '__main__':
    random.seed(12342)
    game = GUI(GameOfLife((10, 10), True, 30), 40, 0.25)
    game.run()