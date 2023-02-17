import pygame
import sys

from overworld import Overworld
from level import Level
from settings import screen_width, screen_height


class Game:
    def __init__(self, surface):
        self.display_surface = surface
        self.max_level = 5
        
        self.overworld = Overworld(self.display_surface, 0, self.max_level, self.create_level)
        self.status = 'overworld'

    def create_level(self, current_level):
        unlock = current_level + 1
        if unlock > 5:
            unlock = 5

        self.level = Level(screen, current_level, unlock, self.create_overworld)
        self.status = 'level'

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level

        self.overworld = Overworld(self.display_surface, current_level, self.max_level, self.create_level)
        self.status = 'overworld'

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        elif self.status == 'level':
            self.level.run()


pygame.init()

pygame.display.set_caption('Treasure Seekers')
pygame.display.set_icon(pygame.image.load('./data/coins/gold/0.png'))

screen = pygame.display.set_mode((screen_width, screen_height), pygame.SCALED)
clock = pygame.time.Clock()

game = Game(screen)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill('grey')

    game.run()

    pygame.display.update()
    clock.tick(60)
