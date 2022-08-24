import pygame
from settings import *
from entity import Entity
from support import *

class Minion(Entity):
    def __init__(self, minion_name, pos, groups, obstacle_sprites, alive_time = 10):
        # general setup
        super().__init__(groups)
        self.sprite_type = 'minion'

        # graphics setup
        # self.import_graphics(minion_name)
        self.fliped = False
        self.status = 'idle'
        self.animations = []
        self.cut_sheet()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations[self.frame_index]
        #self.image = pygame.Surface((TILESIZE, TILESIZE))

        # movement
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites

        # minion stats
        self.minion_name = minion_name
        self.attack_raidus = 100
        self.notice_radius = 300
        self.teleport_radius = 500
        self.speed = 3
        self.alive_duration = alive_time * 1000
        self.alive_time = pygame.time.get_ticks()

        # player interaction
        self.can_teleport = True
        self.teleport_time = None
        self.teleport_cooldown = 3000

    def cut_sheet(self):
        minion_sheet = pygame.image.load(resource_path('assets/graphics/minions/cat.png')).convert_alpha()
        for x in range(2):
            for y in range(1):
                temp_img = minion_sheet.subsurface(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
                self.animations.append(temp_img)

    def get_player_distance_direction(self, player):
        # get player to minion distance and direction
        minion_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - minion_vec).magnitude()
        # converting vector to distance
        if distance > 0:
            direction = (player_vec - minion_vec).normalize()
            # converting vector to unit vector
        else:
            direction = pygame.math.Vector2()
            # vector(0, 0)

        return (distance, direction)

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_raidus:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        elif distance >= self.teleport_radius and self.can_teleport:
            self.can_teleport = False
            self.teleport_time = pygame.time.get_ticks()
            self.status = 'teleport'
        else:
            self.status = 'idle'
    
    def actions(self, player):
        if self.status == 'attack':
            # talk action
            self.direction.x = 0
            self.direction.y = 0
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        elif self.status == 'teleport':
            self.hitbox.x = player.hitbox.x
            self.hitbox.y = player.hitbox.y
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        animation = self.animations
        if self.status == 'move':
            if self.direction.x >= 0:self.fliped = False
            else:self.fliped = True
            self.frame_index = (self.frame_index + self.animation_speed) % len(animation)
        else:
            self.frame_index = 0
        self.image = pygame.transform.flip(animation[int(self.frame_index)], self.fliped, False)
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if pygame.time.get_ticks() - self.alive_time >= self.alive_duration -5000:
            alpha = self.wave_value()
            # toggle alpha from 0 ~ 255
            self.image.set_alpha(alpha)

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        # teleport cooldown
        if not(self.can_teleport):
            if current_time - self.teleport_time >= self.teleport_cooldown:
                self.can_teleport = True
        if current_time - self.alive_time >= self.alive_duration:
            self.kill()

    def update(self):
        self.move(self.speed)
        self.cooldown()
        self.animate()

    def minion_update(self, player):
        self.get_status(player)
        self.actions(player)