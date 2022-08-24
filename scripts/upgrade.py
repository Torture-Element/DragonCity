import pygame
from settings import *

class Upgrade:
    def __init__(self, player, ui, render):
        # general setup
        self.render = render
        
        self.player = player
        self.attribute_number = len(player.stats)
        self.attribute_names = list(player.stats.keys())
        self.max_values = list(player.max_stats.values())
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # column dimensions and creation
        self.height = screen.get_size()[1] * 0.8
        self.width = screen.get_size()[0] // (self.attribute_number + 1)
        self.create_column()

        # selection system
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True
        self.ui = ui

    def input(self):
        keys = pygame.key.get_pressed()

        if self.can_move:
            if keys[pygame.K_RIGHT]:
                self.selection_index = (self.selection_index + 1) % self.attribute_number
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_LEFT]:
                self.selection_index = (self.selection_index + self.attribute_number - 1) % self.attribute_number
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

            if keys[pygame.K_SPACE]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.column_list[self.selection_index].trigger(self.player, True, self.ui)
            elif keys[pygame.K_LSHIFT]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.column_list[self.selection_index].trigger(self.player, False, self.ui)

    def selection_cooldown(self):
        if not(self.can_move):
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 300:
                self.can_move = True

    def create_column(self):
        self.column_list = []

        for column, index in enumerate(range(self.attribute_number)):
            # horizontal position
            full_width = screen.get_size()[0]
            increment = full_width // self.attribute_number
            left = (column * increment) + (increment - self.width) // 2

            # vertical position
            top = screen.get_size()[1] * 0.1

            # create the object
            column = Column(left, top, self.width, self.height, index, self.font)
            self.column_list.append(column)

    def display(self):
        self.input()
        self.selection_cooldown()

        for index, column in enumerate(self.column_list):
            # get attributes
            name = self.attribute_names[index]
            value = self.player.get_value_by_index(index)
            max_value = self.max_values[index]
            cost = self.player.get_cost_by_index(index)
            column.display(screen, self.selection_index, name, value, max_value, cost)
        self.render()

class Column:
    def __init__(self, left, top, width, height, index, font):
        self.rect = pygame.Rect(left, top, width, height)
        self.index = index
        self.font  = font

    def display_names(self, surface, name, cost, selected):
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR

        # title
        title_surf = self.font.render(name, False, color)
        title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0, 20))

        # cost
        cost_surf = self.font.render(f'{int(cost)}', False, color)
        cost_rect = cost_surf.get_rect(midbottom = self.rect.midbottom - pygame.math.Vector2(0, 20))

        # draw
        surface.blit(title_surf, title_rect)
        surface.blit(cost_surf, cost_rect)
    
    def display_slide_bar(self, surface, value, max_value, selected):
        # drawing setup
        top = self.rect.midtop + pygame.math.Vector2(0, 60)
        bottom = self.rect.midbottom - pygame.math.Vector2(0, 60)
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR

        # bar setup
        full_height = bottom[1] - top[1]
        relative_number = (value / max_value) * full_height# like ratio
        value_rect = pygame.Rect(top[0] - 15, bottom[1] - relative_number, 30, 10)

        # draw element
        pygame.draw.line(surface, color, top, bottom, 10)
        pygame.draw.rect(surface, color, value_rect)

    def trigger(self, player, opt, ui):
        upgrade_attribute = list(player.stats.keys())[self.index]

        if opt:
            if player.exp >= player.upgrade_cost[upgrade_attribute]  and player.stats[upgrade_attribute] < player.max_stats[upgrade_attribute]:
                player.exp -= player.upgrade_cost[upgrade_attribute]
                player.stats[upgrade_attribute] *= 1.2
                player.upgrade_cost[upgrade_attribute] *= 1.4

            if player.stats[upgrade_attribute] > player.max_stats[upgrade_attribute]:
                player.stats[upgrade_attribute] = player.max_stats[upgrade_attribute]
        else :
            player.exp += player.upgrade_cost[upgrade_attribute]
            player.stats[upgrade_attribute] /= 1.2
            player.upgrade_cost[upgrade_attribute] /= 1.4
        if upgrade_attribute == 'speed':
            player.speed = player.stats[upgrade_attribute]
        elif upgrade_attribute == 'health':
            # player.health = player.stats['health']
            player.health_bar_length = player.stats[upgrade_attribute] * 2
            player.health_ratio = player.stats['health'] / player.health_bar_length
        elif upgrade_attribute == 'energy':
            player.energy_bar_length = (player.stats[upgrade_attribute] + 10) * 2
            player.energy_ratio = player.stats['energy'] / player.energy_bar_length
        elif upgrade_attribute == 'stamina':
            player.stamina_bar_length = (player.stats[upgrade_attribute] + 10) * 2
            player.stamina_ratio = player.stats['stamina'] / player.stamina_bar_length

        #ui.__init__()

    def display(self, surface, selection_num, name, value, max_value, cost):
        if self.index == selection_num:
            pygame.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
        else:
            pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)

        self.display_names(surface, name, cost, self.index == selection_num)
        self.display_slide_bar(surface, value, max_value, self.index == selection_num)