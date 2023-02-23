import pygame
import sys

from overworld import Overworld
from level import Level
from settings import screen_width, screen_height
from ui import UI


class Game:
    def __init__(self, surface):
        self.display_surface = surface

        self.max_level = 0
        self.max_health = 100
        self.current_health = 100
        self.coins = 0

        self.ui = UI(surface)
        
        self.overworld = Overworld(self.display_surface, 0, self.max_level, self.create_level)
        self.status = 'overworld'

    def create_level(self, current_level):
        unlock = current_level + 1
        if unlock > 5:
            unlock = 5

        self.level = Level(screen, current_level, unlock, self.create_overworld, self.change_coins, self.change_health)
        self.status = 'level'

    def create_overworld(self, current_level, new_max_level, game_over=False):
        if new_max_level > self.max_level:
            self.max_level = new_max_level

        if game_over:
            self.max_level = 0
            self.current_health = 100
            self.coins = 0

        self.overworld = Overworld(self.display_surface, current_level, self.max_level, self.create_level)
        self.status = 'overworld'

    def change_coins(self, amount):
        self.coins += amount

    def change_health(self, amount):
        self.current_health += amount

    def check_game_over(self):
        if self.current_health <= 0:
            self.max_level = 0
            self.current_health = 100
            self.coins = 0

            self.overworld = Overworld(self.display_surface, 0, self.max_level, self.create_level)
            self.status = 'overworld'

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        elif self.status == 'level':
            self.level.run()
            self.ui.show_health(self.current_health, self.max_health)
            self.ui.show_coins(self.coins)
            self.check_game_over()


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
    screen.fill('black')

    game.run()

    pygame.display.update()
    clock.tick(60)
