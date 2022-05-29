import pygame
import pygame_menu
import os

import Settings
import PlayerClass

from Button import Button
from Settings import load_image

pygame.init()

# pygame.key.set_repeat(200, 70)

# создание холста и установка его разрешения
screen = pygame.display.set_mode((1280, 700))
pygame.display.set_caption("Socoban")

FPS = Settings.FPS
WIDTH = Settings.WIDTH
HEIGHT = Settings.HEIGHT
tile_height = tile_width = Settings.tile_height

SPEED = Settings.SPEED
pos_x = 0
pos_y = 0
clock = Settings.clock
level_path = Settings.level_path

all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
box_group = pygame.sprite.Group()

aqua = pygame.Color('#00FFFF')


# images
tiles_images = {'wall': Settings.load_image("wall.png", -1),
                'empty_gray': Settings.load_image("ground_gray.png"),
                'empty_green': Settings.load_image("ground_green.png"),
                'start_pos_green': Settings.load_image("ground_start_pos_gray.png"),
                'start_pos_gray': Settings.load_image("ground_start_pos_green.png"),
                'goal': Settings.load_image("goal.png", -1)}
player_image = Settings.load_image("player_down0.png")
box_images = {'box': Settings.load_image("box_default.png"),
              'box_on_goal': Settings.load_image("box_on_goal.png")}

wall_images = load_image('wall.png', -1)
bg = load_image('background.jpg')


# метод загрузки уровня
def load_level(name):
    fullname = os.path.join('res/levels/', name)
    with open(fullname, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    return list(level_map)


# игровое поле
def play():
    global pos_x, pos_y

    player = PlayerClass.Player(SPEED, pos_x, pos_y, screen)
    player_group.add(player)

    running = True
    while running:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player.rect[0] > 1 and player.possibility_move('left', wall_group):
            player.draw_player('left')
            # player.player_move('left')
        elif keys[pygame.K_RIGHT] and player.rect[0] < WIDTH and player.possibility_move('right', wall_group):
            player.draw_player('right')
            # player.player_move('right')
        elif keys[pygame.K_UP] and player.rect[1] > 1 and player.possibility_move('up', wall_group):
            player.draw_player('up')
            # player.player_move('up')
        elif keys[pygame.K_DOWN] and player.rect[1] < HEIGHT and player.possibility_move('down', wall_group):
            player.draw_player('down')
            # player.player_move('down')
        else:
            player.frame = 0
            # player.player_move('')
            player.draw_player('')

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
                pygame.quit()

        clock.tick(FPS)
        screen.fill('gray')
        tiles_group.draw(screen)
        tiles_group.update()
        wall_group.draw(screen)
        wall_group.update()
        all_sprites.draw(screen)
        all_sprites.update()
        # player_group.draw(screen)
        # player_group.update()
        pygame.display.update()
        pygame.display.flip()


# генерация уровня
def generate_level(level):
    print('generate_level')
    global pos_x, pos_y

    level = load_level(level)

    screen.blit(Settings.load_image('background.jpg'), (0, 0))

    pos_x = pos_y = 0

    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '@':
                pos_y = y * tile_width
                pos_x = x * tile_height
            elif level[y][x] == '.':
                Tile('goal', x, y)
            elif level[y][x] == '$':
                Box(x, y)
            elif level[y][x] == '*':
                BoxOnGoal(x, y)
            elif level[y][x] == '#':
                tile = Tile('wall', x, y)
                wall_group.add(tile)
            elif level[y][x] == ' ':
                Tile('empty_gray', x, y)

    print(all_sprites)
    print(tiles_group)
    print(player_group)
    all_sprites.draw(screen)
    player_group.draw(screen)
    tiles_group.draw(screen)

    play()


# default box
class Box(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = box_images['box']
        self.rect = self.image.get_rect().move(tile_width * x, tile_height * y)

    def checkNextPos(self, directory_of_movement):
        '''я создаю новый экз'''
        if directory_of_movement == 'right':
            tester = Box(self.rect[0] + SPEED, self.rect[1])
        elif directory_of_movement == 'left':
            tester = Box(self.rect[0] - SPEED, self.rect[1])
        elif directory_of_movement == 'up':
            tester = Box(self.rect[1] - SPEED, self.rect[0])
        else:
            tester = Box(self.rect[1] + SPEED, self.rect[0])

        if Box == pygame.sprite.spritecollideany(tester, box_group):
            tester.kill()


# box on goal
class BoxOnGoal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = box_images['box_on_goal']
        self.rect = self.image.get_rect().move(tile_width * x, tile_height * y)


# tile
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, x, y):
        super().__init__(tiles_group)
        self.image = tiles_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * x, tile_height * y)


# стартовое меню
def start_menu():
    print('start_menu')
    menu = pygame_menu.Menu("Main Menu", WIDTH, HEIGHT)
    menu.add.text_input('Nick - ', default='Steve')
    menu.add.button('Play', level_selecter)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(screen)
    screen.blit(Settings.load_image('background_sl.jpg'), (0, 0))


# меню выбора уровня
def level_selecter():
    print('level_selecter')
    pygame.display.set_caption("Level Selecter")
    screen.blit(Settings.load_image('background_sl.jpg'), (0, 0))

    show = True

    while show:
        levels = os.listdir(level_path)

        mouse = pygame.mouse.get_pos()

        buttons = []

        for i in range(len(levels)):
            button = Button(None, (162, 150 + 62 * i), levels[i],
                            pygame.font.SysFont('opensansregular', 30),
                            base_color='white', hovering_color='aqua')
            button.changeColor(mouse)
            button.update(screen)
            buttons.append(button)

        back = Button(None, (1000, 500), 'Back', pygame.font.SysFont('opensansregular', 30),
                      base_color='white', hovering_color='aqua')
        back.changeColor(mouse)
        back.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(buttons)):
                    if buttons[i].checkForInput(mouse):
                        generate_level(levels[i])
                        show = False
                    elif back.checkForInput(mouse):
                        start_menu()
                        show = False

        clock.tick(FPS)
        pygame.display.update()


start_menu()
