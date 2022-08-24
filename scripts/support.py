from csv import reader
from os import walk
import pygame
from settings import resource_path

def import_csv_layout(path):
    terrain_map = []
    with open(resource_path(path)) as level_map:
        layout = reader(level_map, delimiter = ',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map

def import_folder(path):
    surface_list = []
    for _, __, img_files in walk(resource_path(path)):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(resource_path(full_path)).convert_alpha()
            surface_list.append(image_surf)
    return surface_list