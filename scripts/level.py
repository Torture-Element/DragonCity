import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice, randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particle import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade
from npc import Npc
from minion import Minion
from menu import Menu
from save_and_load import found_save_or_not
from dialog import Dialog_box

class Level:
    def __init__(self, render):
        # get the display surface
        self.render = render
        self.game_paused = False
        
        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # dialog
        self.dialog = Dialog_box(render)

        # sprite setup
        self.create_map()
        
        # save
        self.has_save = False
        found_save_or_not(self)

        # user interface
        self.ui = UI()
        self.upgrade = Upgrade(self.player, self.ui, render) # upgrade menu
        self.menu_state = 'none'
        self.menu = Menu(self, render)
        self.prev_menu_state = 'none'
        self.menu_list = self.menu.button_names

        # particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

    def create_map(self):
        # map system
        layouts = {
            'boundary' : import_csv_layout('assets/map/map_FloorBlocks.csv'),
            'grass' : import_csv_layout('assets/map/map_Grass.csv'),
            'objects' : import_csv_layout('assets/map/map_Objects.csv'),
            'entities': import_csv_layout('assets/map/map_Entities.csv')
        }
        graphics = {
            'grass' : import_folder('assets/graphics/Grass'),
            'objects' : import_folder('assets/graphics/objects')
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        # boundary blocks
                        if style == 'boundary':
                            Tile(
                                (x, y), 
                                [self.obstacle_sprites,
                                # self.visible_sprites
                                ], 
                                'invisible'
                                )
                        if style == 'grass':
                            # create a grass tile
                            random_grass_image = choice(graphics['grass'])
                            Tile(
                                (x, y), 
                                [self.visible_sprites, 
                                self.obstacle_sprites, 
                                self.attackable_sprites], 
                                'grass', 
                                random_grass_image
                                )
                        if style == 'objects':
                            # create an object tile
                            surf = graphics['objects'][int(col)]
                            Tile((x, y), 
                            [self.visible_sprites, 
                            self.obstacle_sprites
                            ], 
                            'object', 
                            surf
                            )
                        if style == 'entities':
                            # create entities
                            if col == '394':
                                # player_id in tile_map
                                self.player = Player(
                                    (x, y),
                                    [self.visible_sprites], 
                                    self.obstacle_sprites, 
                                    self.create_attack, 
                                    self.destroy_attack,
                                    self.create_magic
                                    )
                                # make player spawn with flicker effect
                                self.player.vulnerable = False
                                self.player.hurt_time = pygame.time.get_ticks() + 1000
                            else:
                                if col == '390': monster_name = 'bamboo'
                                elif col == '391': monster_name = 'spirit'
                                elif col == '392': monster_name = 'raccoon'
                                elif col == '393': monster_name = 'squid'
                                Enemy(
                                    monster_name, 
                                    (x, y), 
                                    [self.visible_sprites, 
                                    self.attackable_sprites,
                                    self.obstacle_sprites], 
                                    self.obstacle_sprites,
                                    self.damage_player,
                                    self.trigger_death_particles,
                                    self.add_xp
                                    )
        Npc('test', 
        (2100, 1300), 
        [self.visible_sprites], 
        self.obstacle_sprites,
        self.dialog
        )

        Minion('test', 
        (2170, 1300), 
        [self.visible_sprites, 
        self.attack_sprites, 
        self.obstacle_sprites
        ], 
        self.obstacle_sprites
        )

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])
    
    def create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(
                self.player, 
                strength, 
                cost, 
                [self.visible_sprites]
                )
        
        if style == 'flame':
            self.magic_player.flame(
                self.player, 
                cost, 
                [self.visible_sprites, 
                self.attack_sprites]
                )

        if style == 'minion':
            if self.magic_player.minion(self.player, cost):
                Minion('cat', 
                (self.player.hitbox.x, self.player.hitbox.y), 
                [self.visible_sprites, 
                self.attack_sprites,
                self.obstacle_sprites
                ], 
                self.obstacle_sprites, 15 * self.player.stats['magic'] / 4)
        # print(style + ' ' + str(strength) + ' ' + str(cost))

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        # for player attack object logic
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                # spritecollide(sprite, group, DOKILL)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        # attack grass
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 60)
                            # leaf particle amount
                            for leaf in range(randint(3, 6)):
                                self.animation_player.create_grass_particles(
                                    pos - offset, 
                                    [self.visible_sprites]
                                )
                            target_sprite.kill()
                        # attack enemy
                        elif target_sprite.sprite_type == 'enemy':
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            # spawn particles
            self.animation_player.create_particles(
                attack_type, 
                self.player.rect.center, 
                [self.visible_sprites]
                )
            if self.player.health <= 0:
                self.game_paused = True
                self.menu_state = 'dead_screen'
                self.menu.__init__(self)
                
    def player_dead(self):
        # perform player dead react
        # if player dead player's exp left half
        left_exp = self.player.exp/2
        left_stats = self.player.stats
        left_mex_stats = self.player.max_stats
        left_upgrade_cost = self.player.upgrade_cost
        self.__init__()
        self.player.exp = left_exp
        self.player.stats = left_stats
        self.player.max_stats = left_mex_stats
        self.player.upgrade_cost = left_upgrade_cost
        self.player.speed = self.player.stats['speed']
        self.player.refresh_stats()

    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particles(particle_type, pos, [self.visible_sprites])

    def add_xp(self, amount):
        self.player.exp += amount

    def toggle_menu(self):
        self.game_paused = not(self.game_paused)

    def upgrade_menu(self):
        self.prev_menu_state = self.menu_state
        if self.menu_state != 'upgrade':
            self.toggle_menu()
            self.menu_state = 'upgrade'
        elif self.menu_state == 'upgrade':
            self.toggle_menu()
            self.menu_state = 'none'

    def title_screen(self):
        self.prev_menu_state = self.menu_state
        if self.menu_state != 'menu' or self.menu_state != 'title' or self.menu_state != 'dead_screen':
            self.toggle_menu()
            self.menu_state = 'menu'
        elif self.menu_state == 'menu' or self.menu_state == 'title' or self.menu_state == 'dead_screen':
            self.toggle_menu()
            self.menu_state  = 'none'

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)
        if self.game_paused:
            # menu system showed
            if self.menu_state == 'upgrade':
                # display upgrade menu
                self.upgrade.display()
            elif self.menu_state == 'title' or self.menu_state == 'menu' or self.menu_state == 'dead_screen':
                self.menu.display()

        else:
            if self.menu_state != 'none':
                self.menu_state = 'none'
            # run the game
            # update and draw the game
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.visible_sprites.npc_update(self.player)
            self.visible_sprites.minion_update(self.player)
            self.player_attack_logic()
            self.render()

    def init(self):
        # sprite setup
        self.__init__(self.render)

class YSortCameraGroup(pygame.sprite.Group):
    # in godot we call it YSort to make 2.5D
    def __init__(self):
        # general setup
        super().__init__()

        # camera offset
        self.offset = pygame.math.Vector2()
        # to stay player in middle of screen. cut it half.
        self.half_screen_width = screen.get_size()[0]//2
        self.half_screen_height = screen.get_size()[1]//2
        # //2 to get divide 2 result in int

        # box camera setup
        # self.camera_borders = {'left': 200, 'right': 200, 'top': 100, 'bottom': 100}
        self.camera_borders = {'left': 400, 'right': 400, 'top': 200, 'bottom': 200}
        camera_boarders_left = self.camera_borders['left']
        camera_boarders_top = self.camera_borders['top']
        camera_boarders_width = screen.get_size()[0]  - (self.camera_borders['left'] + self.camera_borders['right'])
        camera_boarders_height = screen.get_size()[1]  - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(camera_boarders_left, camera_boarders_top, camera_boarders_width, camera_boarders_height)

        # creating the floor/ground
        self.floor_surf = pygame.image.load(resource_path('assets/graphics/tilemap/ground.png')).convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0, 0))

        # camera speed
        self.keyboard_speed = 5
        self.mouse_speed = 0.4

        # zoom
        self.zoom_scale = 1
        # don't set too large would be lag
        self.internal_surface_size = (WIDTH * 1.5, HEIGHT * 1.5)
        self.internal_surface = pygame.Surface(self.internal_surface_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_surface.get_rect(center = (self.half_screen_width, self.half_screen_height))
        self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surface_size)
        self.internal_offset = pygame.math.Vector2() # need to add after all offset: ground and every object
        self.internal_offset.x = self.internal_surface_size[0] // 2 - self.half_screen_width
        self.internal_offset.y = self.internal_surface_size[1] // 2 - self.half_screen_height

        self.zoom_scale_mininum = WIDTH/self.internal_surface_size[0] # change to large scale
        self.zoom_scale_maxinum = self.internal_surface_size[0]/WIDTH
        # self.zoom_scale_mininum = 0.5 # change to large scale
        # self.zoom_scale_maxinum = 2

    def center_target_camera(self, target):
        # put target at camera center
        # self.offset.x = player.rect.centerx - self.half_screen_width
        # self.offset.y = player.rect.centery - self.half_screen_height
        self.offset.x = target.rect.centerx - self.half_screen_width
        self.offset.y = target.rect.centery - self.half_screen_height

    def box_target_camera(self, target):
        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right
        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom

        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']

    def keyboard_control_camera(self):
        keys = pygame.key.get_pressed()
        # ver 1 only for keyboard
        # if keys[pygame.K_a]:self.offset.x -= self.keyboard_speed
        # if keys[pygame.K_d]:self.offset.x += self.keyboard_speed
        # if keys[pygame.K_w]:self.offset.y -= self.keyboard_speed
        # if keys[pygame.K_s]:self.offset.y += self.keyboard_speed
            
        # ver 2 for keyboard and camera box
        if keys[pygame.K_a]:self.camera_rect.x -= self.keyboard_speed
        if keys[pygame.K_d]:self.camera_rect.x += self.keyboard_speed
        if keys[pygame.K_w]:self.camera_rect.y -= self.keyboard_speed
        if keys[pygame.K_s]:self.camera_rect.y += self.keyboard_speed
        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']

    def mouse_control_camera(self):
        # mouse setting
        pygame.event.set_grab(True) # make mouse can't leave screen anymore
        mouse = pygame.math.Vector2(pygame.mouse.get_pos())
        mouse_offset_vector = pygame.math.Vector2()

        left_border = self.camera_borders['left']
        top_border = self.camera_borders['top']
        right_border = screen.get_size()[0] - self.camera_borders['right']
        bottom_border = screen.get_size()[1] - self.camera_borders['bottom']

        if top_border < mouse.y < bottom_border:
            if mouse.x < left_border:
                mouse_offset_vector.x = mouse.x - left_border
                pygame.mouse.set_pos((left_border, mouse.y))
            if mouse.x > right_border:
                mouse_offset_vector.x = mouse.x - right_border
                pygame.mouse.set_pos((right_border, mouse.y))
        elif mouse.y < top_border:
            if mouse.x < left_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(left_border, top_border)
                pygame.mouse.set_pos((left_border, top_border))
            if mouse.x > right_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(right_border, top_border)
                pygame.mouse.set_pos((right_border, top_border))
        elif mouse.y > bottom_border:
            if mouse.x < left_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(left_border, bottom_border)
                pygame.mouse.set_pos((left_border, bottom_border))
            if mouse.x > right_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(right_border, bottom_border)
                pygame.mouse.set_pos((right_border, bottom_border))

        if left_border < mouse.x < right_border:
            if mouse.y < top_border:
                mouse_offset_vector.y = mouse.y - top_border
                pygame.mouse.set_pos((mouse.x, top_border))
            if mouse.y > bottom_border:
                mouse_offset_vector.y = mouse.y - bottom_border
                pygame.mouse.set_pos((mouse.x, bottom_border))

        # self.offset += mouse_offset_vector * self.mouse_speed # ver 1 for only mouse
        self.camera_rect.x += mouse_offset_vector.x * self.mouse_speed
        self.camera_rect.y += mouse_offset_vector.y * self.mouse_speed

    def zoom_keyboard_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_EQUALS]:
            self.zoom_scale += 0.1
        if keys[pygame.K_MINUS]:
            self.zoom_scale -= 0.1
        if keys[pygame.K_0]:
            self.zoom_scale = 1

    def custom_draw(self, player):
        # getting the offset
        # self.center_target_camera(player) # center camera
        self.box_target_camera(player) # camera box
        self.keyboard_control_camera()
        self.zoom_keyboard_control()
        # self.mouse_control_camera()

        # limit scale size
        if self.zoom_scale < self.zoom_scale_mininum:
            self.zoom_scale = self.zoom_scale_mininum
        elif self.zoom_scale > self.zoom_scale_maxinum:
            self.zoom_scale = self.zoom_scale_maxinum

        self.internal_surface.fill(WATER_COLOR)
        
        # drawing the floor
        # offset needed
        floor_offset_pos = self.floor_rect.topleft - self.offset + self.internal_offset
        # screen.blit(self.floor_surf, floor_offset_pos)
        self.internal_surface.blit(self.floor_surf, floor_offset_pos)

        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            # use sort to create the YSort. and now it has overlap.
            # for camera sprite.rect need to add a offset. 
            # and offset comes from player
            # offset needed
            offset_pos = sprite.rect.topleft - self.offset + self.internal_offset
            # to make camera direction right need to subtract offset
            # screen.blit(sprite.image, offset_pos)
            self.internal_surface.blit(sprite.image, offset_pos)

        scaled_surf  = pygame.transform.scale(self.internal_surface, self.internal_surface_size_vector * self.zoom_scale)
        scaled_rect = scaled_surf.get_rect(center = (self.half_screen_width, self.half_screen_height))

        screen.blit(scaled_surf, scaled_rect)
        
        # camera box line
        # pygame.draw.rect(screen, 'yellow', self.camera_rect, 5)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)

    def npc_update(self, player):
        npc_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'npc']
        for npc in npc_sprites:
            npc.npc_update(player)

    def minion_update(self, player):
        minion_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'minion']
        for minion in minion_sprites:
            minion.minion_update(player)