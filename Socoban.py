import pygame
import pygame_menu
import os

pygame.init()
# pygame.key.set_repeat(200, 70)

# создание холста и установка его разрешения
size = width, height = (1280, 700)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Socoban")

FPS = 50
WIDTH = 1280
HEIGHT = 700
clock = pygame.time.Clock()
level_path = os.getcwd() + '\\res\\levels\\'

player = None
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()


# метод загрузки изображений
def load_image(name, colorkey=None):
    fullname = os.getcwd() + ''.join('\\res\\images\\' + name)
    image = pygame.image.load(fullname).convert()
    # делаем фон прозрачным
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# метод загрузки уровня
def load_level(name):
    fullname = os.path.join('res/levels/', name)
    with open(fullname, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


# images
tiles_images = {'wall': load_image("wall.png"),
                'empty_gray': load_image("ground_gray.png"),
                'empty_green': load_image("ground_green.png"),
                'start_pos_green': load_image("ground_start_pos_gray.png"),
                'start_pos_gray': load_image("ground_start_pos_green.png"),
                'goal': load_image("goal.png")}
player_image = {'player': load_image("player_right.png")}
box_images = {'box': load_image("box_default.png"),
              'box_on_goal': load_image("box_on_goal.png")}
tile_height = tile_width = 64


# default box
class Box(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = box_images[0]
        self.rect = self.image.get_rect().move(tile_width * x, tile_height * y)


# box on goal
class BoxOnGoal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = box_images[1]
        self.rect = self.image.get_rect().move(tile_width * x, tile_height * x)


# tile
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tiles_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


# player
class Player(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(player_group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width,
                                sheet.get_height)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    # переопределяем метод update
    def update(self):
        self.cur_frame = (self.cur_frame + 1 % len(self.frames))
        if self.cur_frame >= len(self.frames):
            self.cur_frame = 0
        self.image = self.frames[self.cur_frame]


# board
# class Board:
#     def __init__(self, width, height):
#         self.width = width
#         self.height = height
#         self.board = [[0] * width for _ in range(height)]
#
#     def set_view(self, left, top, cell_size):
#         self.left = left
#         self.top = top
#         self.cell_size = cell_size
#
#     def render(self):
#         return 0


# генерация уровня
def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '@':
                pass
            elif level[y][x] == '.':
                Tile('empty_green', x, y)
            elif level[y][x] == '$':
                Box(x, y)
            elif level[y][x] == '*':
                BoxOnGoal(x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)


def start_menu():
    menu = pygame_menu.Menu('Welcome', WIDTH, HEIGHT, theme=pygame_menu.themes.THEME_GREEN)
    menu.add.text_input('Nick', default='Nickname')
    menu.add.button('Select Level', select_level)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    menu.mainloop(screen)


def select_level():

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEMOTION:
                print('Поз мыши - ', event.pos)

        pygame.display.flip()


start_menu()

