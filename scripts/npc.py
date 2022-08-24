import pygame
from settings import *
from entity import Entity
from support import *
from debug import debug

class Npc(Entity):
    def __init__(self, npc_name, pos, groups, obstacle_sprites, dialog):
        # general setup
        super().__init__(groups)
        self.sprite_type = 'npc'

        # graphics setup
        # self.import_graphics(npc_name)
        self.status = 'idle'
        # self.image = self.animations[self.status][self.frame_index]
        # self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.or_image = pygame.image.load(resource_path('assets/graphics/npcs/npc_1.png'))
        self.image = self.or_image.copy()

        # movement
        self.spawn_pos = pos
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites

        # npc stats
        self.npc_name = npc_name
        self.talk_raidus = 100
        self.notice_radius = 300
        self.line = 'hello'
        self.speed = 3

        # animation talking bubble
        self.talking_bubble = []
        self.cut_spritesheet()
        self.frame_index = 0
        self.animation_speed = 0.05

        # player interaction
        self.can_talk = True
        self.talk_time = None
        self.talk_cooldown = 400

        # dialog
        self.dialog = dialog
        self.line_index = 0
        self.language = 'english'
        self.languages = ['english', 'tchinese', 'schinese']
        self.language_index = 0
        self.lines_en = ['Hello there.', 'It\'s a good day huh.', 'Good luck for slaying monsters.', 'There are many dead around here.']
        self.lines_tch = ["你好，冒險者", "今天天氣真不錯", "祝你武運昌隆", "最近這裡有不少弟兄葬身於此"]
        self.lines_sch = ["你好，冒险者", "今天天气真不错", "祝你武运昌隆", "最近这里有不少弟兄葬身于此"]
        self.lines = self.lines_en
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # key cooldown
        self.can_press_key = True
        self.press_key_time = None
        self.press_key_cd = 200

        # sound section
        self.speak_sound = pygame.mixer.Sound(resource_path('assets/audio/menu4.wav'))
        self.speak_sound.set_volume(0.3)

    def cut_spritesheet(self):
        bubble_sheet = pygame.image.load(resource_path('assets/graphics/npcs/DialogInfo.png')).convert_alpha()
        for y in range(1):
            # x for direction
            for x in range(4):
                # y for frame
                temp_img = bubble_sheet.subsurface(x * 20, y * 16, 20, 16)
                self.talking_bubble.append(pygame.transform.scale(temp_img, (40, 32)))

    def get_player_distance_direction(self, player):
        # get player to npc distance and direction
        npc_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - npc_vec).magnitude()
        # converting vector to distance
        if distance > 0:
            direction = (player_vec - npc_vec).normalize()
            # converting vector to unit vector
        else:
            direction = pygame.math.Vector2()
            # vector(0, 0)

        return (distance, direction)

    def get_spawnpos_distance_direction(self, pos):
        npc_vec = pygame.math.Vector2(self.rect.center)
        pos_vec = pygame.math.Vector2(pos)
        distance = (pos_vec - npc_vec).magnitude()
        # converting vector to distance
        if distance > 0:
            direction = (pos_vec - npc_vec).normalize()
            # converting vector to unit vector
        else:
            direction = pygame.math.Vector2()
            # vector(0, 0)

        return (distance, direction)

    def get_status(self, player):
        player_distance = self.get_player_distance_direction(player)[0]
        spawn_dist = self.get_spawnpos_distance_direction(self.spawn_pos)[0]

        if player_distance <= self.talk_raidus and self.can_talk:
            if self.status != 'talk':
                self.frame_index = 0
            self.status = 'talk'
        elif player_distance <= self.notice_radius and spawn_dist < 100:
            self.status = 'move_to_player'
            if player_distance < 10 or spawn_dist >= 90:
                self.status = 'idle'
        elif spawn_dist > 50:
            self.status = 'move_to_spawn'
        else:
            self.status = 'idle'
    
    def actions(self, player):
        if self.status == 'talk':
            # check which language choose
            debug(self.language, screen.get_size()[0] - 100, 10)

            # talk action
            self.direction = pygame.math.Vector2()
            self.keyboard_input()
            if self.dialog.show_textbox:
                self.dialog.display()
        else:
            if self.dialog.show_textbox:
                self.dialog.show_textbox = False
                self.line_index = 0
                self.dialog.refresh_lines()
            
            if self.status == 'move_to_player':
                self.direction = self.get_player_distance_direction(player)[1]
            elif self.status == 'move_to_spawn':
                self.direction = self.get_spawnpos_distance_direction(self.spawn_pos)[1]
            else:
                self.direction = pygame.math.Vector2()

    def keyboard_input(self):
        keys = pygame.key.get_pressed()
        if self.can_press_key:
            if keys[pygame.K_t]:
                self.press_key_time = pygame.time.get_ticks()
                self.can_press_key = False
                self.dialog.refresh_lines()
                self.dialog.show_textbox = True
                self.dialog.typing = True
                self.dialog.add_line(self.lines[self.line_index])
                self.speak_sound.play()
            if keys[pygame.K_RETURN]:
                self.press_key_time = pygame.time.get_ticks()
                self.can_press_key = False
                if self.dialog.show_textbox and not(self.dialog.typing):
                    if self.line_index < len(self.lines) - 1:
                        self.line_index += 1
                        self.dialog.add_line(self.lines[self.line_index])
                        self.dialog.typing = True
                        self.speak_sound.play()
                    elif self.line_index == len(self.lines) - 1:
                        self.line_index = 0
                        self.dialog.show_textbox = False
                        self.status = 'idle'
            if keys[pygame.K_y]:
                self.press_key_time = pygame.time.get_ticks()
                self.can_press_key = False
                self.language_index = (self.language_index + 1)  % len(self.languages)
                self.language = self.languages[self.language_index]
                self.language_change()
                
                # self.line_index = 0

    def language_change(self):
        if self.language == 'english':
            self.lines = self.lines_en
        elif self.language == 'tchinese':
            self.lines = self.lines_tch
        elif self.language == 'schinese':
            self.lines = self.lines_sch        

    def animation(self):
        if self.status == 'talk':
            self.frame_index = (self.frame_index + self.animation_speed) % len(self.talking_bubble)
            bubble = self.talking_bubble[int(self.frame_index)]
            self.image.blit(bubble, (0, 0))
            self.dialog.blit_press_hint()
            # if npc can talk merge bubble on npc.
        else:self.image = self.or_image.copy()

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        # talk cooldown
        if not(self.can_talk):
            if current_time - self.talk_time >= self.talk_cooldown:
                self.can_talk = True

        if not(self.can_press_key):
            if current_time - self.press_key_time >= self.press_key_cd:
                self.can_press_key = True


    def update(self):
        self.animation()
        self.move(self.speed)
        self.cooldown()

    def npc_update(self, player):
        self.get_status(player)
        self.actions(player)