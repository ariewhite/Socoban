import pygame

from Settings import load_image

pygame.init()
surface = pygame.display.set_mode((1, 1))

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


class Player(pygame.sprite.Sprite):

    def __init__(self, speed, x, y, screen):
        super().__init__()
        self.speed = speed
        self.frame = 0
        self.cur_frame = 0
        self.image = animation_down[0]
        self.screen = screen
        self.rect = self.image.get_rect().move(x, y)
        self.radius = 28
        self.directory_of_move = ''
        self.ration = 0

    # move
    def next_movement(self):
        if self.directory_of_move == 'right':
            self.rect[0] += 64
        elif self.directory_of_move == 'left':
            self.rect[0] -= 64
        elif self.directory_of_move == 'up':
            self.rect[1] -= 64
        elif self.directory_of_move == 'down':
            self.rect[1] += 64
        self.ration += 1

    # draw
    def draw_player(self, directory_of_movement):

        if self.frame + 1 > 30:
            self.frame = 0

        if directory_of_movement == 'left':
            self.cur_frame = self.frame // 5
            self.image = animation_left[self.cur_frame]
            self.screen.blit(self.image, (self.rect[0], self.rect[1]))
            self.frame += 1
            self.rect[0] -= self.speed
            print('player - ', self.rect)
        elif directory_of_movement == 'right':
            self.cur_frame = self.frame // 5
            self.image = animation_right[self.cur_frame]
            self.screen.blit(self.image, (self.rect[0], self.rect[1]))
            self.frame += 1
            self.rect[0] += self.speed
            print('player - ', self.rect)
        elif directory_of_movement == 'up':
            self.cur_frame = self.frame // 5
            self.image = animation_up[self.cur_frame]
            self.screen.blit(self.image, (self.rect[0], self.rect[1]))
            self.frame += 1
            self.rect[1] -= self.speed
            print('player - ', self.rect)
        elif directory_of_movement == 'down':
            self.cur_frame = self.frame // 5
            self.image = animation_down[self.cur_frame]
            self.screen.blit(self.image, (self.rect[0], self.rect[1]))
            self.frame += 1
            self.rect[1] += self.speed
            print('player - ', self.rect)
        else:
            self.screen.blit(animation_down[0], (self.rect[0], self.rect[1]))

        self.update()
        pygame.display.update()

    def possibility_move(self, directory_of_movement):
        if directory_of_movement == 'right':
            tester = Player(self.speed, self.rect[0] + self.speed, self.rect[1], self.screen)
            tester.directory_of_move = 'right'
        elif directory_of_movement == 'left':
            tester = Player(self.speed, self.rect[0] - self.speed, self.rect[1], self.screen)
            tester.directory_of_move = 'left'
        elif directory_of_movement == 'up':
            tester = Player(self.speed, self.rect[0], self.rect[1] - self.speed, self.screen)
            tester.directory_of_move = 'up'
        else:
            tester = Player(self.speed, self.rect[0], self.rect[1] + self.speed, self.screen)
            tester.directory_of_move = 'down'

        return tester
