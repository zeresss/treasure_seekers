import pygame

from support import import_folder
from decorations import Sky


class Node(pygame.sprite.Sprite):
    def __init__(self, pos, status, path):
        super().__init__()
        self.frames = import_folder(path)
        self.animation_frame = 0

        self.image = self.frames[self.animation_frame]
        self.rect = self.image.get_rect(center=pos)

        self.status = status
        self.stop_zone = pygame.Rect(self.rect.centerx - 4, self.rect.centery - 4, 8, 8)

    def animate(self):
        self.animation_frame += 0.1
        if self.animation_frame >= len(self.frames):
            self.animation_frame = 0
        self.image = self.frames[int(self.animation_frame)]

    def update(self):
        if self.status == 'available':
            self.animate()
        else:
            dark = self.image.copy()
            dark.fill('black', None, pygame.BLEND_RGBA_MULT)
            self.image.blit(dark, (0, 0))


class PlayerIcon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.image = pygame.image.load('./data/player/hat.png').convert_alpha()
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.rect.center = self.pos


class Overworld:
    def __init__(self, surface, current_level, max_level, create_level):
        self.display_surface = surface
        self.direction = pygame.Vector2(0, 0)
        self.key_cooldown = 1
        self.sky = Sky(surface, 12, 8, 'overworld')
        self.nodes_pos = [(110, 400), (300, 220), (480, 610), (610, 350), (880, 210), (1050, 400)]

        self.current_level = current_level
        self.max_level = max_level
        self.create_level = create_level

        self.nodes_setup()

        self.player_icon = pygame.sprite.GroupSingle()
        player_icon_sprite = PlayerIcon(self.nodes.sprites()[self.current_level].rect.center)
        self.player_icon.add(player_icon_sprite)

    def nodes_setup(self):
        self.nodes = pygame.sprite.Group()
        for node_index, node_pos in enumerate(self.nodes_pos):
            if node_index <= self.max_level:
                node_sprite = Node(node_pos, 'available', f'./data/overworld/{node_index}')
            else:
                node_sprite = Node(node_pos, 'locked', f'./data/overworld/{node_index}')
            self.nodes.add(node_sprite)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if not self.direction and self.key_cooldown >= 5:
            if keys[pygame.K_d] and self.current_level < self.max_level:
                self.direction = self.get_movement_data(1)
                self.current_level += 1
            elif keys[pygame.K_a] and self.current_level > 0:
                self.direction = self.get_movement_data(-1)
                self.current_level -= 1
            elif keys[pygame.K_SPACE]:
                self.create_level(self.current_level)

        self.key_cooldown += 1

    def get_movement_data(self, movement):
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
        end = pygame.math.Vector2(self.nodes.sprites()[self.current_level + movement].rect.center)
        return (end - start).normalize()

    def update_icon_pos(self):
        if self.direction:
            self.player_icon.sprite.pos += self.direction * 8
            target_node = self.nodes.sprites()[self.current_level]
            if target_node.stop_zone.collidepoint(self.player_icon.sprite.pos):
                self.direction = pygame.math.Vector2(0, 0)

    def draw_paths(self):
        points = [node_pos for node_index, node_pos in enumerate(self.nodes_pos) if node_index <= self.max_level]

        if self.max_level > 0:
            pygame.draw.lines(self.display_surface, '#a04f45', False, points, 6)

    def run(self):
        self.get_input()
        self.sky.draw()
        self.draw_paths()
        self.nodes.update()
        self.nodes.draw(self.display_surface)
        self.update_icon_pos()
        self.player_icon.update()
        self.player_icon.draw(self.display_surface)
