import pygame

from support import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, collision_sprites):
        super().__init__()
        self.collision_sprites = collision_sprites

        self.direction = pygame.math.Vector2()
        self.status, self.facing = 'idle', 'right'
        self.on_ground, self.on_ceiling = False, False
        self.crouching = False

        self.animations = {'idle': [], 'walk': [], 'jump': [], 'fall': []}
        for animation in self.animations.keys():
            full_path = './data/player/animations/' + animation
            self.animations[animation] = import_folder(full_path)
        self.animation_frame = 0

        self.image = self.animations[self.status][self.animation_frame]
        self.rect = self.image.get_rect(topleft=pos)
        self.collision_rect = pygame.Rect(self.rect.topleft, (50, self.rect.height))

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.direction.x = -6
            self.facing = 'left'
        elif keys[pygame.K_d]:
            self.direction.x = 6
            self.facing = 'right'
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.direction.y = -16

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        elif self.direction.x != 0:
            self.status = 'walk'
        else:
            self.status = 'idle'

    def animate(self):
        animation = self.animations[self.status]

        self.animation_frame += 0.1
        if self.animation_frame >= len(animation):
            self.animation_frame = 0

        if self.facing == 'right':
            self.image = animation[int(self.animation_frame)]
            self.rect.bottomleft = self.collision_rect.bottomleft
        elif self.facing == 'left':
            self.image = pygame.transform.flip(animation[int(self.animation_frame)], True, False)
            self.rect.bottomright = self.collision_rect.bottomright

        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def horizontal_collisions(self):
        self.collision_rect.x += self.direction.x

        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.collision_rect):
                if self.direction.x < 0:
                    self.collision_rect.left = sprite.rect.right
                elif self.direction.x > 0:
                    self.collision_rect.right = sprite.rect.left

    def vertical_collisions(self):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.collision_rect):
                if self.direction.y < 0:
                    self.collision_rect.top = sprite.rect.bottom
                    self.direction.y = 0
                    self.on_ceiling = True
                elif self.direction.y > 0:
                    self.collision_rect.bottom = sprite.rect.top
                    self.direction.y = 0
                    self.on_ground = True

        if self.on_ground and self.direction.y < 0 or self.direction.y > 1:
            self.on_ground = False
        if self.on_ceiling and self.direction.y > 1:
            self.on_ceiling = False

    def apply_gravity(self):
        self.direction.y += 0.8
        self.collision_rect.y += self.direction.y

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.horizontal_collisions()
        self.apply_gravity()
        self.vertical_collisions()
