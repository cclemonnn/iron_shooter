from settings import TILE_SIZE
from pygame.sprite import Group

from support import import_csv_layout, import_cut_graphics
from tiles import StaticTile


class Level:
    def __init__(self, level_data, surface):
        # general set up
        self.display_surface = surface
        self.world_shift = 0

        # terrain
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        # grass
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        # palms
        palms_layout = import_csv_layout(level_data['fg palms'])
        self.palms_sprites = self.create_tile_group(grass_layout, 'fg palms')

    def create_tile_group(self, layout, image_type):
        sprite_group = Group()

        for row_index, row in enumerate(layout):
            for column_index, item in enumerate(row):
                if item != '-1':
                    x = column_index * TILE_SIZE
                    y = row_index * TILE_SIZE

                    if image_type == 'terrain':
                        terrain_image_list = import_cut_graphics('images/terrains/terrain_tiles.png')
                        tile_surface = terrain_image_list[int(item)]
                        sprite = StaticTile(TILE_SIZE, x, y, tile_surface)
                        sprite_group.add(sprite)

                    elif image_type == 'grass':
                        grass_image_list = import_cut_graphics('images/grass/grass.png')
                        tile_surface = grass_image_list[int(item)]
                        sprite = StaticTile(TILE_SIZE, x, y, tile_surface)
                        sprite_group.add(sprite)


        return sprite_group

    def draw(self):
        # draw terrain
        self.terrain_sprites.draw(self.display_surface)

        # draw grass
        self.grass_sprites.draw(self.display_surface)

    def update(self, movement):
        # update terrain
        self.terrain_sprites.update(movement)
        # update grass
        self.grass_sprites.update(movement)

