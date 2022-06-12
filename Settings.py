import pygame
import os
import sqlite3

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
cur_level = 0
# ------------path--------------------
level_path = os.getcwd() + '\\res\\levels\\'
stat_path = os.getcwd() + '\\res\\statistics.dontopen'

try:
    sqlite_connection = sqlite3.connect('sqlite_python.db')
    cursor = sqlite_connection.cursor()
    print("База данных создана и успешно подключена к SQLite")

    sqlite_select_query = "create table if not exists users (" \
                          "count_of_movement INTEGER)"
    cursor.execute(sqlite_select_query)
    sqlite_connection.commit()

except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite", error)


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
    cursor.execute("select * from users")
    cursor.execute(f"insert into users values ({count_of_moves})")
    sqlite_connection.commit()

    print('vse okey')


def get_statistics():
    global count_of_moves
    for value in cursor.execute("select * from users"):
        count_of_moves = value
