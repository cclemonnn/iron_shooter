from csv import reader

import pygame.image
from pygame.rect import Rect
from pygame.surface import Surface

from settings import TILE_SIZE


def import_csv_layout(csv_path):
    terrain_map = []
    with open(csv_path) as map:
        level = reader(map, delimiter=',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map


def import_cut_graphics(image_path):
    # loads image
    surface = pygame.image.load(image_path).convert_alpha()

    # measure image tiles
    tile_x = surface.get_size()[0] // TILE_SIZE
    tile_y = surface.get_size()[1] // TILE_SIZE

    cut_tiles = []
    for row in range(tile_y):
        for col in range(tile_x):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            # flags = source alpha: set unused parts to invisible
            new_surface = Surface((TILE_SIZE, TILE_SIZE), flags=pygame.SRCALPHA)
            new_surface.blit(surface, (0, 0), Rect(x, y, TILE_SIZE, TILE_SIZE))
            cut_tiles.append(new_surface)

    return cut_tiles
