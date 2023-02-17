import pygame
from random import choice, randint

from settings import screen_width, tile_size
from support import import_folder


class Sky:
    def __init__(self, surface, height, horizon, style):
        self.display_surface = surface
        self.height = height
        self.horizon = horizon
        self.style = style

        self.sky_top = pygame.transform.scale(pygame.image.load('./data/decorations/sky/top.png'),
                                              (screen_width, tile_size))
        self.sky_bottom = pygame.transform.scale(pygame.image.load('./data/decorations/sky/bottom.png'),
                                                 (screen_width, tile_size))
        self.sky_middle = pygame.transform.scale(pygame.image.load('./data/decorations/sky/middle.png'),
                                                 (screen_width, tile_size))

        if style == 'overworld':
            palm_surfaces = import_folder('./data/overworld/palms')
            self.palms_sprites = []

            for surface in [choice(palm_surfaces) for _ in range(10)]:
                x = randint(0, screen_width)
                y = (self.horizon * tile_size) + randint(50, 100)

                rect = surface.get_rect(midbottom=(x, y))
                self.palms_sprites.append((surface, rect))

            cloud_surfaces = import_folder('./data/overworld/clouds')
            self.clouds_sprites = []

            for surface in [choice(cloud_surfaces) for _ in range(10)]:
                x = randint(0, screen_width)
                y = randint(0, (self.horizon * tile_size) - 100)

                rect = surface.get_rect(midbottom=(x, y))
                self.clouds_sprites.append((surface, rect))

    def draw(self):
        for row in range(self.height):
            y = row * tile_size

            if row < self.horizon:
                self.display_surface.blit(self.sky_top, (0, y))
            elif row == self.horizon:
                self.display_surface.blit(self.sky_middle, (0, y))
            else:
                self.display_surface.blit(self.sky_bottom, (0, y))
        if self.style == 'overworld':
            for palm in self.palms_sprites:
                self.display_surface.blit(palm[0], palm[1])
            for cloud in self.clouds_sprites:
                self.display_surface.blit(cloud[0], cloud[1])
