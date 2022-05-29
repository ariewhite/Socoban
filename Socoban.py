import os
import pygame


pygame.init()


clock = pygame.time.Clock()
WIDHT = 800
HEIGHT = 600
FPS = 30
SPEED = 5

screen = pygame.display.set_mode((WIDHT, HEIGHT))


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


animation_right = [load_image('player_right0.png', -1),
                   load_image('player_right1.png', -1),
                   load_image('player_right2.png', -1),
                   load_image('player_right1.png', -1),
                   load_image('player_right2.png', -1),
                   load_image('player_right0.png', -1)]
animation_left = [load_image('player_left0.png', -1),
                  load_image('player_left1.png', -1),
                  load_image('player_left2.png', -1),
                  load_image('player_left1.png', -1),
                  load_image('player_left2.png', -1),
                  load_image('player_left0.png', -1)]
animation_up = [load_image('player_up0.png', -1),
                load_image('player_up1.png', -1),
                load_image('player_up2.png', -1),
                load_image('player_up1.png', -1),
                load_image('player_up2.png', -1),
                load_image('player_up0.png', -1)]
animation_down = [load_image('player_down0.png', -1),
                  load_image('player_down1.png', -1),
                  load_image('player_down2.png', -1),
                  load_image('player_down1.png', -1),
                  load_image('player_down2.png', -1),
                  load_image('player_down0.png', -1)]

wall_images = load_image('wall.png', -1)

frame = 0
pos_x = 10
pos_y = 10
left = False
right = False
up = False
down = False

player_group = pygame.sprite.Group()
other_group = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(other_group)
        self.image = wall_images
        self.rect = self.image.get_rect().move(x, y)


class Player(pygame.sprite.Sprite):
    def __init__(self, speed, x, y):
        super().__init__(player_group)
        self.speed = speed
        self.frames = []
        self.cur_frame = 0
        self.image = animation_down[0]
        self.rect = self.image.get_rect().move(x, y)
        self.rect[0] = float(self.rect[0])
        self.rect[1] = float(self.rect[1])


    def draw_player(self):
        global pos_x, pos_y
        global right, left, up, down
        global frame

        if frame + 1 > 30:
            frame = 0

        if left:
            self.cur_frame = frame // 5
            self.image = animation_left[self.cur_frame]
            screen.blit(self.image, (pos_x, pos_y))
            frame += 1
        elif right:
            self.cur_frame = frame // 5
            self.image = animation_right[self.cur_frame]
            screen.blit(self.image, (pos_x, pos_y))
            frame += 1
        elif up:
            self.cur_frame = frame // 5
            self.image = animation_up[self.cur_frame]
            screen.blit(self.image, (pos_x, pos_y))
            frame += 1
        elif down:
            self.cur_frame = frame // 5
            self.image = animation_down[self.cur_frame]
            screen.blit(self.image, (pos_x, pos_y))
            frame += 1
        else:
            screen.blit(animation_down[0], (pos_x, pos_y))

        self.update()
        pygame.display.update()

    def update(self):
        self.rect = self.image.get_rect().move(pos_x + self.speed, pos_y + self.speed)
        print('player - ', self.rect)

    def dorabotat_possibility_move(self, directory_of_movement):
        if directory_of_movement == 'right':
            tester = Player(self.speed, self.rect[0] + self.speed, self.rect[1])
        elif directory_of_movement == 'left':
            tester = Player(self.speed, self.rect[0] - self.speed, self.rect[1])
        elif directory_of_movement == 'up':
            tester = Player(self.speed, self.rect[1] - self.speed, self.rect[0])
        else:
            tester = Player(self.speed, self.rect[1] + self.speed, self.rect[0])

        if pygame.sprite.spritecollide(tester, other_group, dokill=False, collided=pygame.sprite.collide_rect_ratio(0.7)):
            print('collision')
            tester.kill()
            return False
        else:
            return True


player = Player(SPEED, pos_x, pos_y)
tile2 = Tile(264, 264)
tile3 = Tile(264+64, 264)

running = True
while running:
    screen.fill('black')
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and pos_x > 5 and player.dorabotat_possibility_move('left'):
        pos_x -= player.speed
        left = True
        right = False
        down = False
        up = False
    elif keys[pygame.K_RIGHT] and pos_x < WIDHT and player.dorabotat_possibility_move('right'):
        pos_x += player.speed
        left = down = up = False
        right = True
    elif keys[pygame.K_UP] and pos_y > 5 and player.dorabotat_possibility_move('up'):
        pos_y -= player.speed
        up = True
        right = left = down = False
    elif keys[pygame.K_DOWN] and pos_y < HEIGHT and player.dorabotat_possibility_move('down'):
        pos_y += player.speed
        left = right = up = False
        down = True
    else:
        left = up = down = right = False
        frame = 0

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()

    clock.tick(FPS)

    other_group.draw(screen)
    other_group.update()
    player.draw_player()
    pygame.display.update()
