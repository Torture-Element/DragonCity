import pygame
from debug import debug
from settings import *
from support import import_folder
from entity import Entity

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic):
        super().__init__(groups)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-6, HITBOX_OFFSET['player']) # change the hitbox

        # graphics setup
        self.sprite_type = 'player'
        self.animations = {
            'up':[], 'down':[], 'left':[], 'right':[],
            'up_idle':[], 'down_idle':[], 'left_idle':[], 'right_idle':[],
            'up_attack':[], 'down_attack':[], 'left_attack':[], 'right_attack':[],
            'up_roll':[], 'down_roll':[], 'left_roll':[], 'right_roll':[]
        }
        self.cut_player_spritesheet()
        self.status = 'down'

        # movement
            # attack
        self.attacking = False
        self.can_attack = True
        self.attack_cooldown = 400
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites
            # tired
        self.tired = False
        self.tired_cooldown = 1000
        self.tired_time = None
            # roll
        self.can_roll = True
        self.rolling = False
        self.rolling_duration = 300
        self.rolling_time = None
        self.roll_cost = 10
        
        # weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        # magic
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        # stats
        self.stats = {'health': 100,'energy':60,'attack': 10,'magic': 4,'speed': 5, 'stamina':100}
        self.max_stats = {'health': 300, 'energy': 140, 'attack': 20, 'magic' : 10, 'speed': 10, 'stamina':200}
        self.upgrade_cost = {'health': 100, 'energy': 100, 'attack': 100, 'magic' : 100, 'speed': 100, 'stamina':100}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.stamina = self.stats['stamina']
        self.speed = self.stats['speed']
        self.exp = 0

        # ui improved
        self.current_health = self.health # for hp animation
        self.health_change_speed = 0.25
        self.health_bar_length = HEALTH_BAR_WIDTH
        self.health_ratio = self.stats['health'] / self.health_bar_length
        self.current_energy = self.energy # for hp animation
        self.energy_change_speed = 0.25
        self.energy_bar_length = ENERGY_BAR_WIDTH
        self.energy_ratio = self.stats['energy'] / self.energy_bar_length
        self.stamina_bar_length = ENERGY_BAR_WIDTH
        self.stamina_ratio = self.stats['stamina'] / self.stamina_bar_length

        # damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

        # import a sound
        self.weapon_attack_sound = pygame.mixer.Sound(resource_path('assets/audio/sword.wav'))
        self.weapon_attack_sound.set_volume(0.01)

    # because i don't like import pic one by one folder.
    # so i abandon this function. though it might be great.
    # def import_player_assets(self):
    #     character_path = 'assets/graphics/player/'
    #     for animation in self.animations.keys():
    #         full_path = character_path + animation
    #         self.animations[animation] = import_folder(full_path)
    
    # remember to use right format: 64*64.
    def cut_player_spritesheet(self):
        # improve old way to import character from folder one by one.
        # only need one character sheet.
        dir = ['down', 'up', 'left', 'right']
        player_sheet = pygame.image.load(resource_path('assets/graphics/player/player_spritesheet.png')).convert_alpha()
        for x, animation in enumerate(dir):
            # x for direction
            for y in range(5):
                # y for frame
                temp_img = player_sheet.subsurface(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
                self.animations[animation + '_roll'].append(pygame.transform.rotate(temp_img, 90 * y))
                if y == 0:
                    self.animations[animation + '_idle'].append(temp_img)
                if y < 4:
                    self.animations[animation].append(temp_img)
                elif y == 4:
                    self.animations[animation + '_attack'].append(temp_img)

    def input(self):
        if not self.attacking and not(self.tired):
            # get player input
            keys = pygame.key.get_pressed()

            # movement input
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0
            
            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            if keys[pygame.K_LSHIFT] and self.can_roll:
                if self.stamina >= self.roll_cost * 100 / self.stats['stamina']:
                    self.stamina_cost(self.roll_cost * 100 / self.stats['stamina'])
                    self.can_roll = False
                    self.rolling = True
                    self.rolling_time = pygame.time.get_ticks()

            # attack input
            if (keys[pygame.K_z] or keys[pygame.K_SPACE]) and self.can_attack:
                if self.stamina >= list(weapon_data.values())[self.weapon_index]['stamina_cost']:
                    self.stamina_cost(list(weapon_data.values())[self.weapon_index]['stamina_cost'])
                    self.attacking = True
                    self.can_attack = False
                    self.attack_time = pygame.time.get_ticks()
                    self.create_attack()
                    self.weapon_attack_sound.play()

            # magic input
            if keys[pygame.K_LCTRL]:
                self.stamina_cost(10)
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[self.magic_index]['cost']
                self.create_magic(style, strength, cost)

            # switch weapon
            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                self.weapon_index = (self.weapon_index + 1) % len(weapon_data)
                self.weapon = list(weapon_data.keys())[self.weapon_index]
                #print(str(self.weapon_index) + ' ' + self.weapon)
            
            # switch magic
            if keys[pygame.K_e] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()
                self.magic_index = (self.magic_index + 1) % len(magic_data)
                self.magic = list(magic_data.keys())[self.magic_index]

    def get_status(self):
        # idle status
        if (self.direction.x == 0 and self.direction.y == 0 and not(self.attacking) and not(self.rolling)) or self.tired:
            self.stamina_recovery(3)
            self.energy_recovery(2)
            if not 'idle' in self.status and not 'attack' in self.status and not'roll' in self.status:
                self.status = self.status + '_idle'
        if not 'idle' in self.status and not 'attack' in self.status and not 'roll' in self.status:
            self.stamina_recovery(0.5 + 0.01 * self.stats['speed'])
            self.energy_recovery(0.5 + 0.01 * self.stats['magic'])

            # walk stamina cost
                # removed because many reporter complained
            # if self.stamina > 0:
            #     self.stamina_cost(0.2 + 0.01 * self.stats['speed'])
        
        if self.rolling and not(self.attacking):
            self.speed = self.stats['speed'] * 3
            if self.speed < 5:
                self.speed = 5
            elif self.speed > 20:
                self.speed = 20
            self.vulnerable = False
            if 'up' in self.status:
                self.direction.x = 0
                self.direction.y = -1
            elif 'down' in self.status:
                self.direction.x = 0
                self.direction.y = 1
            elif 'left' in self.status:
                self.direction.x = -1
                self.direction.y = 0
            elif 'right' in self.status:
                self.direction.x = 1
                self.direction.y = 0

            if not 'roll' in self.status:
                if 'idle' in self.status:
                    # overwrite idle
                    self.status = self.status.replace('idle', 'roll')
                else:
                    self.status = self.status + '_roll'
        else:
            if 'roll' in self.status:
                self.status = self.status.replace('_roll','')

        if self.attacking and not(self.rolling):
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    # overwrite idle
                    self.status = self.status.replace('idle', 'attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack','')

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        # attack cooldown
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown'] - self.stats['stamina'] * 0.1 - self.stats['attack'] * 0.2:
                self.attacking = False
                self.destroy_attack()
        # cooldown after attack
        if not(self.can_attack):
            if current_time - self.attack_time >= 2*(self.attack_cooldown + weapon_data[self.weapon]['cooldown']) - self.stats['stamina'] * 0.5:
                self.can_attack = True

        # switch weapon cooldown
        if not(self.can_switch_weapon):
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        # switch magic cooldown
        if not(self.can_switch_magic):
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True

        # get hit timer
        if not(self.vulnerable):
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

        # tired timer
        if self.tired:
            if current_time - self.tired_time >= self.tired_cooldown:
                self.tired = False

        # rolling timer
        if self.rolling:
            if current_time - self.rolling_time >= self.rolling_duration:
                self.rolling = False
                self.speed = self.stats['speed']
        if not(self.can_roll):
            if current_time - self.rolling_time >= self.rolling_duration * 2 * self.health / self.stats['health']:
                self.can_roll = True

    def animate(self):
        animation = self.animations[self.status]
        # loop over the frame index
        self.frame_index = (self.frame_index + self.animation_speed) % len(animation)

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        # get hit flicker animation
        if not self.vulnerable:
            alpha = self.wave_value()
            # toggle alpha from 0 ~ 255
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage

    def get_full_magic_damage(self):
        base_damage = self.stats['magic']
        spell_damage = magic_data[self.magic]['strength']
        return base_damage + spell_damage

    def get_value_by_index(self, index):
        return list(self.stats.values())[index]
    
    def get_cost_by_index(self, index):
        return list(self.upgrade_cost.values())[index]

    def energy_recovery(self, rate):
        if self.energy < self.stats['energy']:
            self.energy = (self.energy + 0.01 * rate * self.stats['magic'])
            if self.energy > self.stats['energy']:
                self.energy = self.stats['energy']

    def stamina_cost(self, cost):
        self.stamina -= cost
        if self.stamina <= 0:
            self.stamina = 0
            self.direction.x = 0
            self.direction.y = 0
            self.tired_time = pygame.time.get_ticks()
            self.tired = True

    def stamina_recovery(self, rate):
        if self.stamina < self.stats['stamina']:
            self.stamina = (self.stamina + 0.002 * rate * self.stats['stamina'])
            if self.stamina > self.stats['stamina']:
                self.stamina = self.stats['stamina']

    def refresh_stats(self):
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.stamina = self.stats['stamina']
        self.speed = self.stats['speed']
        self.current_health = self.health # for hp animation
        self.health_bar_length = self.stats['health'] * 2
        self.health_ratio = self.stats['health'] / self.health_bar_length
        self.current_energy = self.energy # for hp animation
        self.energy_bar_length = self.stats['energy'] * 2
        self.energy_ratio = self.stats['energy'] / self.energy_bar_length
        self.stamina_bar_length = self.stats['stamina'] * 2
        self.stamina_ratio = self.stats['stamina'] / self.stamina_bar_length
    
    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)