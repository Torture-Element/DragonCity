import os, sys
import pygame

pygame.init()

# for packing game
def resource_path(relative):
	if hasattr(sys, "_MEIPASS"):
		absolute_path = os.path.join(sys._MEIPASS, relative)
	else:
		absolute_path = os.path.join(relative)
	return absolute_path

# game setup
WIDTH    = 1280
HEIGHT   = 720
VIRTUAL_RES = (800, 600)
REAL_RES = (WIDTH, HEIGHT)
FPS      = 60
TILESIZE = 64
HITBOX_OFFSET = {
    'player': -26,
    'object': -40,
    'grass': -10,
    'invisible': 0
    }
screen = pygame.Surface(VIRTUAL_RES).convert((255, 65280, 16711680, 0))

# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = resource_path('assets/graphics/font/joystix.ttf')
UI_FONT_SIZE = 18
 
# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'
 
# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
STAMINA_COLOR = 'green'
UI_BORDER_COLOR_ACTIVE = 'gold'

# upgrade menu
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'

# weapons
weapon_data = {
    'sword': {'cooldown': 100, 'damage': 15, 'stamina_cost':15,'graphic':'assets/graphics/weapons/all_weapons/sword_full.png'},
    'lance': {'cooldown': 200, 'damage': 30, 'stamina_cost':25, 'graphic':'assets/graphics/weapons/all_weapons/lance_full.png'},
    'axe': {'cooldown': 150, 'damage': 20, 'stamina_cost':20, 'graphic':'assets/graphics/weapons/all_weapons/axe_full.png'},
    'rapier' : {'cooldown': 50, 'damage': 8, 'stamina_cost':8, 'graphic':'assets/graphics/weapons/all_weapons/rapier_full.png'},
    'sai' : {'cooldown': 80, 'damage': 10, 'stamina_cost':4, 'graphic':'assets/graphics/weapons/all_weapons/sai_full.png'}
    }
# another way to import weapon image
    # weapon_image = {
    #     'sword': {'up':[], 'down':[], 'left':[], 'right':[]},
    #     'lance': {'up':[], 'down':[], 'left':[], 'right':[]},
    #     'axe': {'up':[], 'down':[], 'left':[], 'right':[]},
    #     'rapier' : {'up':[], 'down':[], 'left':[], 'right':[]},
    #     'sai' : {'up':[], 'down':[], 'left':[], 'right':[]}
    # }
    # for weapon in list(weapon_data.keys()):
    #     weapon_image[weapon]

# magic
magic_data = {
    'flame': {'strength': 5,'cost': 20,'graphic':'assets/graphics/particles/flame/fire.png'},
    'heal' : {'strength': 20,'cost': 10,'graphic':'assets/graphics/particles/heal/heal.png'},
    'minion' : {'strength': 60,'cost': 10,'graphic':'assets/graphics/minions/cat.png'}
}

# enemy
monster_data = {
    'squid': {'health': 100,'exp':100,'damage':20,'attack_type': 'slash', 'attack_sound':'assets/audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
    'raccoon': {'health': 300,'exp':250,'damage':40,'attack_type': 'claw',  'attack_sound':'assets/audio/attack/claw.wav','speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
    'spirit': {'health': 100,'exp':110,'damage':8,'attack_type': 'thunder', 'attack_sound':'assets/audio/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
    'bamboo': {'health': 70,'exp':120,'damage':6,'attack_type': 'leaf_attack', 'attack_sound':'assets/audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300}
    }