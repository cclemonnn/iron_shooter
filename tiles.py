from pygame.sprite import Sprite
from pygame.surface import Surface

'''class for tile images and updates'''


class Tile(Sprite):
    def __init__(self, tile_size, x, y):
        super().__init__()
        self.image = Surface((tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self, shift):
        self.rect.x += shift


class StaticTile(Tile):
    def __init__(self, tile_size, x, y, surface):
        super().__init__(tile_size, x, y)
        self.image = surface
