import pygame
from os import walk
from csv import reader

from settings import tile_size


def import_folder(path, reversed=False):
    surface_list = []
    for _, _, image_files in walk(path):
        for image in image_files:
            image_surface = pygame.transform.flip(pygame.image.load(f'{path}/{image}').convert_alpha(), reversed, False)
            surface_list.append(image_surface)
    return surface_list


def import_csv_layout(path):
    terrain_map = []
    with open(path) as file:
        level = reader(file, delimiter=',')
        for row in level:
            terrain_map.append(list(row))
    return terrain_map


def import_cut_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_width() / tile_size)
    tile_num_y = int(surface.get_height() / tile_size)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size

            new_surface = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
            new_surface.blit(surface, (0, 0), pygame.Rect(x, y, tile_size, tile_size))
            cut_tiles.append(new_surface)
    return cut_tiles
