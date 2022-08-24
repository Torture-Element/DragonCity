import pygame
from settings import resource_path

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.sprite_type = 'weapon'
        direction = player.status.split('_', 1)[0]
        dir = {'up':0, 'left':1, 'down':2, 'right':3}
        # split('@', times) -> seperate string with @ and do times
        # times can without but for safe i add one.
        # and also i just need first word. so i use [0].

        # graphic
        full_path = f'assets/graphics/weapons/all_weapons/{player.weapon}_half.png'
        #full_path = f'assets/graphics/weapons/{player.weapon}/{direction}.png'
        self.image = pygame.image.load(resource_path(full_path)).convert_alpha()
        self.image = pygame.transform.rotate(self.image, 90 * dir[direction])
        # self.image = pygame.Surface((40, 40)) # test black block

        # placement
        if direction == 'right':
            self.rect =  self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(-5, 16))
            # add offset make weapon pos little lower.
        elif direction == 'left':
            self.rect =  self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(5, 16))
        elif direction == 'down':
            self.rect =  self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-10, -5))
        elif direction == 'up':
            self.rect =  self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-14, 5))
        else:
            self.rect = self.image.get_rect(center = player.rect.center)