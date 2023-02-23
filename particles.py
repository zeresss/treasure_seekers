import pygame

from support import import_folder


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, path, flipped=False):
        super().__init__()
        self.frames = import_folder(path, flipped)
        self.animation_frame = 0

        self.image = self.frames[self.animation_frame]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        self.animation_frame += 0.5
        if self.animation_frame >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.animation_frame)]

    def update(self):
        self.animate()
