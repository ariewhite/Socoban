import pygame
import pygame_menu
import os
import plyer
import sqlite3

import Settings
import PlayerClass

from Button import Button
from Settings import load_image

pygame.init()

# pygame.key.set_repeat(200, 70)

# создание холста и установка его разрешения
screen = pygame.display.set_mode((1280, 700))
pygame.display.set_caption("Socoban")

# ------------consts-----------------
FPS = Settings.FPS
WIDTH = Settings.WIDTH
HEIGHT = Settings.HEIGHT
tile_height = tile_width = Settings.tile_height

SPEED = Settings.SPEED
pos_x = 0
pos_y = 0
clock = Settings.clock
level_path = Settings.level_path
# ------------groups-----------------
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
box_group = pygame.sprite.Group()
box_on_goal = pygame.sprite.Group()
goal_group = pygame.sprite.Group()
all_group = []
boxs = []
goals = []
# ------------colors-----------------
aqua = pygame.Color('#00FFFF')
dark_gray = pygame.Color('#A9A9A9')

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
level_bg = load_image('level_bg.jpg')


# метод загрузки уровня
def load_level(name):
    fullname = os.path.join('res/levels/', name)
    with open(fullname, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    return list(level_map)


# игровое поле
def play():
    player = PlayerClass.Player(SPEED, pos_x, pos_y, screen)
    player_group.add(player)

    running = True
    while running:
        keys = pygame.key.get_pressed()
        pygame.mixer.music.load(os.getcwd() + '\\res\\sounds\\run.mp3')

        if keys[pygame.K_LEFT] and player.rect[0] > 1 and collision_movement(player.possibility_move('left')):
            player.draw_player('left')
            pygame.mixer.music.play(0, fade_ms=1)
            Settings.count_of_moves += 1
        elif keys[pygame.K_RIGHT] and player.rect[0] < WIDTH and collision_movement(player.possibility_move('right')):
            player.draw_player('right')
            pygame.mixer.music.play(0, fade_ms=2)
            Settings.count_of_moves += 1
        elif keys[pygame.K_UP] and player.rect[1] > 1 and collision_movement(player.possibility_move('up')):
            player.draw_player('up')
            pygame.mixer.music.play(0, fade_ms=3)
            Settings.count_of_moves += 1
        elif keys[pygame.K_DOWN] and player.rect[1] < HEIGHT and collision_movement(player.possibility_move('down')):
            player.draw_player('down')
            pygame.mixer.music.play(0, fade_ms=4)
            Settings.count_of_moves += 1
        elif keys[pygame.K_ESCAPE]:
            level_selecter()
            running = False
        elif keys[pygame.K_r]:
            generate_level(Settings.cur_level)
            running = False
        else:
            player.frame = 0
            player.draw_player('')

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
                pygame.quit()

        clock.tick(FPS)

        update_level()

        state_level()


def collision_movement(tester):
    if pygame.sprite.spritecollide(tester, wall_group,
                                   collided=pygame.sprite.collide_rect_ratio(0.8), dokill=False):
        print('collision with wall')
        tester.kill()
        return False
    elif pygame.sprite.spritecollideany(tester, box_group):
        sprite1 = pygame.sprite.spritecollideany(tester, box_group)
        print('collision with box')
        for box in boxs:
            if pygame.sprite.collide_rect(box, sprite1):
                tester.next_movement()
                if box.checkNextPos(tester):
                    box.go_move(tester.directory_of_move)
                    return False

            return True
    elif pygame.sprite.spritecollide(tester, box_on_goal,
                                     collided=pygame.sprite.collide_rect_ratio(0.9), dokill=False):
        print('collision with box _ on goal')
        tester.kill()
        return True
    else:
        return True

    tester.kill()


def state_level():
    for box in box_group:
        if pygame.sprite.spritecollide(box, goal_group, dokill=False):
            box.image = box_images['box_on_goal']
    for goal in goal_group:
        if goal.complet:
            continue

        if pygame.sprite.spritecollide(goal, box_group, dokill=False):
            goal.complet = True
        else:
            goal.complet = False

    count_box_on_goal = 0
    for goal in goal_group:
        if goal.complet:
            count_box_on_goal += 1
    if count_box_on_goal == len(goal_group):
        level_complete()


# update level
def update_level():
    screen.blit(level_bg, (0, 0))
    all_sprites.draw(screen)
    tiles_group.draw(screen)
    box_group.draw(screen)
    goal_group.draw(screen)
    wall_group.draw(screen)
    pygame.display.update()


# генерация уровня
def generate_level(level):
    print('generate_level')
    global pos_x, pos_y
    Settings.cur_level = level
    level = load_level(level)

    screen.blit(Settings.load_image('background.jpg'), (0, 0))

    pos_x = pos_y = 0

    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '@':
                pos_y = y * tile_width
                pos_x = x * tile_height
            elif level[y][x] == '.':
                goal = Goal(x, y)
                goals.append(goal)
            elif level[y][x] == '$':
                box = Box(x, y)
                boxs.append(box)
            elif level[y][x] == '*':
                box = Box(x, y)
                boxs.append(box)
                goal = Goal(x, y)
                goals.append(goal)
            elif level[y][x] == '#':
                tile = Tile('wall', x, y)
                wall_group.add(tile)
            elif level[y][x] == ' ':
                Tile('empty_gray', x, y)

    all_group.append(wall_group)
    all_group.append(box_group)
    all_group.append(box_on_goal)

    all_sprites.draw(screen)
    player_group.draw(screen)
    tiles_group.draw(screen)

    play()


# default box
class Box(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, box_group)
        self.image = box_images['box']
        self.rect = self.image.get_rect().move(tile_width * x, tile_height * y)

    @staticmethod
    def checkNextPos(tester):
        if pygame.sprite.spritecollide(tester, wall_group,
                                       collided=pygame.sprite.collide_rect_ratio(0.8), dokill=False):
            print('next collision with wall')
            return False
        else:
            return True

    def go_move(self, directory_of_movement):
        if directory_of_movement == 'right':
            self.rect[0] += SPEED
        elif directory_of_movement == 'left':
            self.rect[0] -= SPEED
        elif directory_of_movement == 'up':
            self.rect[1] -= SPEED
        else:
            self.rect[1] += SPEED

        self.update()


# box on goal
class BoxOnGoal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, box_on_goal)
        self.image = box_images['box_on_goal']
        self.rect = self.image.get_rect().move(tile_width * x, tile_height * y)


# tile
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, x, y):
        super().__init__(all_sprites, tiles_group)
        self.image = tiles_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * x, tile_height * y)


# goal
class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, goal_group)
        self.image = tiles_images['goal']
        self.rect = self.image.get_rect().move(x * tile_width, y * tile_height)
        self.complet = False


# стартовое меню
def start_menu():
    # ------------sounds-----------------
    pygame.mixer.music.load(os.getcwd() + '\\res\\sounds\\fon.mp3')
    pygame.mixer.music.play(-1)

    # ------------menu-----------------
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

        statistic = Button(None, (1000, 600), 'Statistics', pygame.font.SysFont('opensansregular', 30),
                           base_color='white', hovering_color='aqua')
        statistic.changeColor(mouse)
        statistic.update(screen)

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
                    elif statistic.checkForInput(mouse):
                        statistics()
                        show = False

        clock.tick(FPS)
        pygame.display.update()


def statistics():
    screen.blit(load_image('background_sl.jpg'), (0, 0))

    show = True
    while show:
        mouse = pygame.mouse.get_pos()

        stat = Button(None, (200, 200), 'count of movement - ' + str(Settings.count_of_moves),
                      pygame.font.SysFont('opensansregular', 30),
                      base_color='white', hovering_color='aqua')
        stat.update(screen)
        stat.changeColor(mouse)
        back = Button(None, (1000, 500), 'Back', pygame.font.SysFont('opensansregular', 30),
                      base_color='white', hovering_color='aqua')
        back.changeColor(mouse)
        back.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back.checkForInput(mouse):
                    level_selecter()
                    show = False

        clock.tick(FPS)
        pygame.display.update()


def level_complete():
    # ------------sounds-----------------
    pygame.mixer.music.load(os.getcwd() + '\\res\\sounds\\level_completed.mp3')
    pygame.mixer.music.play(0)

    Settings.load_statistics()
    Settings.get_statistics()

    plyer.notification.notify(message='Level Completed',
                              app_name='Socoban',
                              title='congratulations!')

    level_selecter()


start_menu()
