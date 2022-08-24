import json

def save_file(level):
    with open('save_file.txt', 'w') as save_file:
        json.dump([level.player.stats, level.player.upgrade_cost, level.player.exp], save_file)

def load_file(level):
    # if level detect has save file than load file
    if level.has_save:
        with open('save_file.txt') as save_file:
            level.player.stats,  level.player.upgrade_cost, level.player.exp = json.load(save_file)

def found_save_or_not(level):
    # check if save_file.txt exist
    try:
        with open('save_file.txt') as save_file:
            level.has_save = True
    except:
        level.has_save = False