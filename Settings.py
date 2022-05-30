import pygame
import os

pygame.init()
# ------------size-----------------
size = width, height = (1280, 700)
# ------------consts-----------------
FPS = 30
WIDTH = 1280
HEIGHT = 700
tile_height = tile_width = 64
SPEED = 5
clock = pygame.time.Clock()
# ------------statistics-----------------
count_of_moves = 0
levels_completed = 0
# ------------path--------------------
level_path = os.getcwd() + '\\res\\levels\\'
stat_path = os.getcwd() + '\\res\\statistics.dontopen'


# метод загрузки изображений
def load_image(name, colorkey=None):
    fullname = (os.getcwd() + ''.join('\\res\\images\\' + name))
    image = pygame.image.load(fullname).convert()
    # делаем фон прозрачным
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_statistics():
    with open(stat_path, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    level_map[0] = str(count_of_moves)
    level_map[1] = str(levels_completed)
