from random import choice

import pygame
from debug import debug
from player import *
from settings import *
from support import *
from tile import Tile
from weapon import Weapon


class Level:
    def __init__(self):

        # Getting the display screen
        self.display_surface = pygame.display.get_surface()
        # Setting up sprite groups
        self.visable_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.create_map()

        #Attack Sprites
        self.current_attack = None

    def create_map(self):
        layouts = {

            'boundary': import_csv_layout('../map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('../map/map_Grass.csv'),
            'object': import_csv_layout('../map/map_Objects.csv')


        }

        graphics = {
            'grass': import_folder('../graphics/Grass'),
            'objects': import_folder('../graphics/objects')
        }

        #print(graphics)

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, collum in enumerate(row):
                    if collum != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisable')
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x, y), [
                                 self.obstacle_sprites, self.visable_sprites], 'grass', random_grass_image)
                        if style == 'object':
                            surface = graphics['objects'][int(collum)]
                            Tile((x, y), [self.obstacle_sprites,
                                 self.visable_sprites], 'object', surface)
        self.player = Player(
            (2000, 1430), [self.visable_sprites], self.obstacle_sprites, self.create_attack, self.destroy_attack)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visable_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
            self.current_attack = None

    def run(self):
        # Update and draw the game
        self.visable_sprites.custom_draw(self.player)
        self.visable_sprites.update()
        debug(self.player.status)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # Making the floor
        self.floor_surface = pygame.image.load(
            '../graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # Drawing floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
