import pygame
from settings import *

class UI:
    def __init__(self):
        # general
        
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar setup
        # self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        # self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)
        # self.stamina_bar_rect = pygame.Rect(10, 58, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        # convert weapon dictionary
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(resource_path(path)).convert_alpha()
            self.weapon_graphics.append(weapon)

        # convert magic dictionary
        self.magic_graphics = []
        for magic in magic_data.values():
            path = magic['graphic']
            magic = pygame.image.load(resource_path(path)).convert_alpha()
            if magic.get_width() > TILESIZE:
                magic = magic.subsurface(0 ,0, TILESIZE, TILESIZE)
            self.magic_graphics.append(magic)

    def show_bar(self, current, max_amount, bg_rect, color):
        # draw bg
        pygame.draw.rect(screen, UI_BG_COLOR, bg_rect)

        # converting stat to pixel
        ratio = current / max_amount
        if ratio > 1:
            ratio = 1
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # drawing the bar
        pygame.draw.rect(screen, color, current_rect)
        pygame.draw.rect(screen, UI_BORDER_COLOR, bg_rect, 3)

    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        x = screen.get_size()[0] - 20
        y = screen.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright = (x, y))

        pygame.draw.rect(screen, UI_BG_COLOR, text_rect.inflate(20, 20))
        screen.blit(text_surf, text_rect)
        pygame.draw.rect(screen, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)

    def selection_box(self, left, top, has_switched):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(screen, UI_BG_COLOR, bg_rect)
        if has_switched:
            pygame.draw.rect(screen, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(screen, UI_BORDER_COLOR, bg_rect, 3)
        return bg_rect

    def weapon_overlay(self, weapon_index, has_switched):
        bg_rect = self.selection_box(10, screen.get_size()[1] - 90, has_switched) # weapon
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center = bg_rect.center)

        screen.blit(weapon_surf, weapon_rect)

    def magic_overlay(self, magic_index, has_switched):
        bg_rect = self.selection_box(80, screen.get_size()[1] - 85, has_switched) # magic
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center = bg_rect.center)

        screen.blit(magic_surf, magic_rect)

    def advanced_health(self, player):
        transition_width = 0
        transition_color = (255, 0, 0)
        health_bar_rect = pygame.Rect(10, 10, player.current_health / player.health_ratio,BAR_HEIGHT)

        if player.current_health < player.health:
            player.current_health += player.health_change_speed
            transition_width = int((player.health - player.current_health) / (player.health_ratio))
            transition_color = (0, 255, 0) # green
        if player.current_health > player.health:
            if player.health < player.stats['health'] / 3:
                # if player health lower than max health / 3 than speed up animation speed
                player.current_health -= player.health_change_speed * 5
            else:
                player.current_health -= player.health_change_speed
            transition_width = int((player.current_health - player.health) / (player.health_ratio))
            transition_color = (255, 255, 0) # yellow
            if health_bar_rect.right + transition_width > player.health_bar_length + 5:
                    transition_width = player.health_bar_length + 5 - health_bar_rect.right

        transition_bar_rect = pygame.Rect(health_bar_rect.right, 10, transition_width, BAR_HEIGHT)

        # black bg
        pygame.draw.rect(screen, UI_BG_COLOR, (10, 10, player.health_bar_length, BAR_HEIGHT))
        # health bar
        pygame.draw.rect(screen, HEALTH_COLOR, health_bar_rect)
        # health bar animation
        pygame.draw.rect(screen, transition_color, transition_bar_rect)
        # outline
        pygame.draw.rect(screen, UI_BORDER_COLOR, (10, 10, player.health_bar_length, BAR_HEIGHT), 3)

    def advanced_magic_bar(self, player):
        transition_width = 0
        transition_color = (255, 0, 0)
        energy_bar_rect = pygame.Rect(10, 34, player.current_energy / player.energy_ratio,BAR_HEIGHT)

        if player.current_energy < player.energy:
            player.current_energy += player.energy_change_speed
            transition_width = int((player.energy - player.current_energy) / (player.energy_ratio))
            transition_color = (0, 255, 0) # green
        if player.current_energy > player.energy:
            player.current_energy -= player.energy_change_speed
            transition_width = int((player.current_energy - player.energy) / (player.energy_ratio))
            transition_color = (255, 255, 0) # yellow
            if energy_bar_rect.right + transition_width > player.energy_bar_length:
                    transition_width = player.energy_bar_length - energy_bar_rect.right

        transition_bar_rect = pygame.Rect(energy_bar_rect.right, 34, transition_width, BAR_HEIGHT)

        # black bg
        pygame.draw.rect(screen, UI_BG_COLOR, (10, 34, player.energy_bar_length, BAR_HEIGHT))
        # energy bar
        pygame.draw.rect(screen, ENERGY_COLOR, energy_bar_rect)
        # energy bar animation
        pygame.draw.rect(screen, transition_color, transition_bar_rect)
        # outline
        pygame.draw.rect(screen, UI_BORDER_COLOR, (10, 34, player.energy_bar_length, BAR_HEIGHT), 3)

    def advanced_stamina_bar(self, player):
        stamina_bar_rect = pygame.Rect(10, 58, player.stamina / player.stamina_ratio,BAR_HEIGHT)

        # black bg
        pygame.draw.rect(screen, UI_BG_COLOR, (10, 58, player.stamina_bar_length, BAR_HEIGHT))
        # stamina bar
        pygame.draw.rect(screen, STAMINA_COLOR, stamina_bar_rect)
        # outline
        pygame.draw.rect(screen, UI_BORDER_COLOR, (10, 58, player.stamina_bar_length, BAR_HEIGHT), 3)


    def display(self, player):
        # health and energy
        self.advanced_health(player) # hp bar with animation
        self.advanced_magic_bar(player)
        self.advanced_stamina_bar(player)
        # old bars
        # self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        # self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)
        # self.show_bar(player.stamina, player.stats['stamina'], self.stamina_bar_rect, STAMINA_COLOR  if not(player.tired) else HEALTH_COLOR)
        
        self.show_exp(player.exp)

        self.weapon_overlay(player.weapon_index, not(player.can_switch_weapon))
        self.magic_overlay(player.magic_index, not(player.can_switch_magic))