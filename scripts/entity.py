import pygame
from math import sin
from settings import TILESIZE

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()

    def move(self, speed):
        # to fix incline speed more faster
        if self.direction.magnitude() != 0:
            # 0 can't be normalized. python will error.
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center
        # you may use this func in other script.
        # so instead use self.speed use speed as reference.
    
    def collision(self, direction):
        # since we can only know we bump in pygame.
        # but we don't know which side bump into. so we need to sort.
        for sprite in self.obstacle_sprites:
            if sprite != self:
                if self.sprite_type == 'player' and (sprite.sprite_type == 'minion' or sprite.sprite_type == 'enemy'):
                    pass
                elif self.sprite_type == 'minion' and sprite.sprite_type == 'enemy':
                    pass
                elif self.sprite_type == 'enemy' and sprite.sprite_type == 'minion':
                    pass
                elif (self.image.get_width() > TILESIZE and self.sprite_type == sprite.sprite_type) or (self.sprite_type == sprite.sprite_type and sprite.image.get_width() > TILESIZE):
                    pass
                else:
                    if direction == 'horizontal':
                        if sprite.hitbox.colliderect(self.hitbox):
                            if self.direction.x > 0: # moving right
                                self.hitbox.right = sprite.hitbox.left
                            if self.direction.x < 0: # moving left
                                self.hitbox.left = sprite.hitbox.right

                    if direction == 'vertical':
                        if sprite.hitbox.colliderect(self.hitbox):
                            if self.direction.y > 0: # moving down
                                self.hitbox.bottom = sprite.hitbox.top
                            if self.direction.y < 0: # moving up
                                self.hitbox.top = sprite.hitbox.bottom

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0
