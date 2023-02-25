import pygame
from random import randint, choice

from support import import_csv_layout, import_cut_graphics, import_folder
from settings import tile_size, screen_width
from tiles import StaticTile, AnimatedTile
from player import Player
from enemy import Enemy
from camera import CameraGroup
from particles import ParticleEffect
from decorations import Sky
from collectables import Collectable


class Level:
    def __init__(self, surface, current_level, unlock, create_overworld, change_coins, change_health):
        self.display_surface = surface

        self.current_level = current_level
        self.new_max_level = unlock
        self.create_overworld = create_overworld

        self.terrain_tile_list = import_cut_graphics('./data/terrain/terrain tiles.png')
        self.grass_tile_list = import_cut_graphics('./data/decorations/grass.png')

        path = f'./data/levels/{current_level}/'
        terrain_layout = import_csv_layout(path + 'terrain.csv')

        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')
        self.grass_sprites = self.create_tile_group(import_csv_layout(path + 'grass.csv'), 'grass')
        self.crate_sprites = self.create_tile_group(import_csv_layout(path + 'crates.csv'), 'crates')
        self.coin_sprites = self.create_tile_group(import_csv_layout(path + 'coins.csv'), 'coins')
        self.palm_sprites = self.create_tile_group(import_csv_layout(path + 'palms.csv'), 'palms')
        self.bg_palms_sprites = self.create_tile_group(import_csv_layout(path + 'bg palms.csv'), 'bg palms')
        self.constraint_sprites = self.create_tile_group(import_csv_layout(path + 'constraints.csv'), 'constraints')
        self.enemy_sprites = self.create_tile_group(import_csv_layout(path + 'enemies.csv'), 'enemies')

        self.level_width = len(terrain_layout[0])
        self.level_height = len(terrain_layout)
        self.pixel_level_width = self.level_width * 64
        self.pixel_level_height = self.level_height * 64

        self.sky = Sky(self.display_surface, self.level_height, 8, 'level')
        self.water_setup()
        self.clouds_setup()

        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.Group()
        self.player_setup(import_csv_layout(path + 'player.csv'), change_health)
        self.change_coins = change_coins

        self.last_status = self.player.sprite.status
        self.last_facing = self.player.sprite.facing

        self.visible_sprites = CameraGroup(self.display_surface)
        self.active_sprites = pygame.sprite.Group()

        self.visible_sprites.add(
            self.cloud_sprites, self.bg_palms_sprites, self.terrain_sprites, self.grass_sprites, self.crate_sprites,
            self.enemy_sprites, self.palm_sprites, self.coin_sprites, self.player, self.goal, self.water_sprites
        )

        self.active_sprites.add(
            self.bg_palms_sprites, self.coin_sprites, self.palm_sprites, self.enemy_sprites, self.player,
            self.water_sprites
        )

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, value in enumerate(row):
                if value != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        sprite = StaticTile((x, y), self.terrain_tile_list[int(value)])

                    elif type == 'grass':
                        sprite = StaticTile((x, y), self.grass_tile_list[int(value)])

                    elif type == 'crates':
                        sprite = StaticTile((x, y + 23),
                                            pygame.image.load('./data/terrain/crate.png').convert_alpha())

                    elif type == 'coins':
                        if value == '0':
                            sprite = Collectable((x + 16, y + 16), './data/coins/gold', 3)
                        elif value == '1':
                            sprite = Collectable((x + 16, y + 16), './data/coins/silver', 1)

                    elif type == 'palms':
                        if value == '2':
                            sprite = AnimatedTile((x, y - int(tile_size / 2)), './data/terrain/palm small')
                        elif value == '1':
                            sprite = AnimatedTile((x, y - tile_size), './data/terrain/palm large')

                    elif type == 'bg palms':
                        sprite = AnimatedTile((x, y - tile_size), './data/terrain/palm bg')

                    elif type == 'enemies':
                        sprite = Enemy((x, y + 18), self.constraint_sprites)

                    elif type == 'constraints':
                        sprite = StaticTile((x, y), pygame.Surface((tile_size, tile_size)))

                    sprite_group.add(sprite)

        return sprite_group

    def player_setup(self, layout, change_health):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size

                if val == '0':
                    sprite = Player((x, y), self.terrain_sprites.sprites() + self.crate_sprites.sprites() +
                                    self.palm_sprites.sprites(), change_health)
                    self.player.add(sprite)

                if val == '1':
                    sprite = StaticTile((x, y), pygame.image.load('./data/player/hat.png').convert_alpha())
                    self.goal.add(sprite)

    def water_setup(self):
        self.water_sprites = pygame.sprite.Group()
        for tile in range(int(self.level_width + self.pixel_level_width / 8)):
            x = tile * 192 - screen_width
            y = tile_size * 11

            sprite = AnimatedTile((x, y), './data/decorations/water')
            self.water_sprites.add(sprite)

    def clouds_setup(self):
        clouds_images = import_folder('./data/decorations/clouds')
        self.cloud_sprites = pygame.sprite.Group()
        for cloud in range(20):
            x = randint(-self.pixel_level_width + int(self.pixel_level_width / 8),
                        self.pixel_level_width + int(self.pixel_level_width / 8))
            y = randint(0, self.pixel_level_height - int(self.pixel_level_width / 8))

            sprite = StaticTile((x, y), choice(clouds_images))
            self.cloud_sprites.add(sprite)

    def draw_player_particles(self):
        if self.player.sprite.status == 'jump' and self.last_status != 'jump':
            if self.player.sprite.facing == 'right':
                offset = pygame.math.Vector2(-14, -13)
            else:
                offset = pygame.math.Vector2(14, -13)
            particle_effect = ParticleEffect(self.player.sprite.rect.midbottom + offset, './data/player/particles/jump')

            self.visible_sprites.add(particle_effect)
            self.active_sprites.add(particle_effect)

        elif self.player.sprite.status == 'idle' and self.last_status == 'fall':
            if self.player.sprite.facing == 'right':
                offset = pygame.math.Vector2(-14, -20)
            else:
                offset = pygame.math.Vector2(14, -20)
            particle_effect = ParticleEffect(self.player.sprite.rect.midbottom + offset, './data/player/particles/land')

            self.visible_sprites.add(particle_effect)
            self.active_sprites.add(particle_effect)

        elif self.player.sprite.status == 'walk' and self.last_status == 'idle' or self.player.sprite.status == 'walk' \
                and self.last_status == 'walk' and self.player.sprite.facing != self.last_facing:
            if self.player.sprite.facing == 'right':
                offset = pygame.math.Vector2(-30, -5)
                particle_effect = ParticleEffect(self.player.sprite.rect.midbottom + offset,
                                                 './data/player/particles/walk')
            else:
                offset = pygame.math.Vector2(30, -5)
                particle_effect = ParticleEffect(self.player.sprite.rect.midbottom + offset,
                                                 './data/player/particles/walk', True)

            self.visible_sprites.add(particle_effect)
            self.active_sprites.add(particle_effect)

        self.last_status = self.player.sprite.status
        self.last_facing = self.player.sprite.facing

    def check_drown(self):
        if self.player.sprite.rect.top > self.pixel_level_height:
            self.create_overworld(0, self.current_level, True)

    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.create_overworld(self.current_level, self.new_max_level)

    def check_coin_receive(self):
        collided_coins = pygame.sprite.spritecollide(self.player.sprite, self.coin_sprites, True)
        for coin in collided_coins:
            self.change_coins(coin.value)

    def check_enemy_kill(self):
        collided_enemies = pygame.sprite.spritecollide(self.player.sprite, self.enemy_sprites, False)
        for enemy in collided_enemies:
            if enemy.rect.top < self.player.sprite.rect.bottom < enemy.rect.centery\
                    and self.player.sprite.direction.y >= 0:
                self.player.sprite.direction.y = -14
                enemy.kill()

                explosion_sprite = ParticleEffect(enemy.rect.center, './data/enemy/explosion')
                self.visible_sprites.add(explosion_sprite)
                self.active_sprites.add(explosion_sprite)
            else:
                self.player.sprite.get_damage()

    def run(self):
        self.sky.draw()
        self.active_sprites.update()
        self.visible_sprites.draw(self.player.sprite)
        self.draw_player_particles()

        self.check_drown()
        self.check_win()
        self.check_coin_receive()
        self.check_enemy_kill()
