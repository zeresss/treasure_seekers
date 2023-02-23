import pygame

from tiles import AnimatedTile


class Collectable(AnimatedTile):
    def __init__(self, pos, path, value):
        super().__init__(pos, path)
        self.value = value