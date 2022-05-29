import pygame
import os

pygame.init()

size = width, height = (1280, 700)

FPS = 30
WIDTH = 1280
HEIGHT = 700
tile_height = tile_width = 64
SPEED = 5

clock = pygame.time.Clock()
level_path = os.getcwd() + '\\res\\levels\\'


name = 'player_right0.png'
print(os.getcwd() + ''.join('\\res\\images\\' + name))

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