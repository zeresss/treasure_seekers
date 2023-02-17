import pygame
from random import randint

from tiles import AnimatedTile


class Enemy(AnimatedTile):
    def __init__(self, pos, reverse_sprites):
        super().__init__(pos, 'data/enemy/run')
        self.reverse_sprites = reverse_sprites
        self.speed = randint(3, 5)

    def move(self):
        self.rect.x += self.speed

    def check_image_reverse(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def check_speed_reverse(self):
        for sprite in self.reverse_sprites:
            if sprite.rect.colliderect(self.rect):
                self.speed = -self.speed

    def update(self):
        self.animate()
        self.move()
        self.check_speed_reverse()
        self.check_image_reverse()
