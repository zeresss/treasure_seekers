import pygame

from support import import_folder
from settings import tile_size


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((tile_size, tile_size))
        self.rect = self.image.get_rect(topleft=pos)


class StaticTile(Tile):
    def __init__(self, pos, surface):
        super().__init__(pos)
        self.image = surface


class AnimatedTile(Tile):
    def __init__(self, pos, path):
        super().__init__(pos)
        self.frames = import_folder(path)
        self.animation_frame = 0
        self.image = self.frames[self.animation_frame]

    def animate(self):
        self.animation_frame += 0.1
        if self.animation_frame >= len(self.frames):
            self.animation_frame = 0
        self.image = self.frames[int(self.animation_frame)]

    def update(self):
        self.animate()
