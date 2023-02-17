import pygame


class CameraGroup(pygame.sprite.Group):
    def __init__(self, surface):
        super().__init__()
        self.display_surface = surface

        self.offset = pygame.math.Vector2()
        self.camera_rect = pygame.Rect(320, 0, 640, 0)

    def draw(self, player):
        if player.collision_rect.left < self.camera_rect.left:
            self.camera_rect.left = player.collision_rect.left
        if player.collision_rect.right > self.camera_rect.right:
            self.camera_rect.right = player.collision_rect.right

        self.offset = pygame.math.Vector2(self.camera_rect.left - 320, self.camera_rect.top)
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
