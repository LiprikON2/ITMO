import pygame
from pygame.locals import *

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

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Создание списка клеток
        # self.grid = self.life.create_grid(randomize=True)
        
        running = True
        while self.life.is_changing and not self.life.is_max_generations_exceed:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            
            # Отрисовка списка клеток
            self.draw_grid()
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.life.step()
            
            self.draw_lines()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

if __name__ == '__main__':
    game = GUI(GameOfLife((4, 4), True, 30), 40, 1)
    game.run()