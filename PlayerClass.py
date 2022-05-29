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

    # # move
    # def player_move(self, directory_of_movement):
    #     if directory_of_movement == 'right':
    #         self.image.get_rect().move(self.rect[0] + self.speed, self.rect[1])
    #         self.rect[0] += self.speed
    #         print('player - ', self.rect)
    #         # self.draw_player('right', self.screen)
    #     elif directory_of_movement == 'left':
    #         self.image.get_rect().move(self.rect[0] - self.speed, self.rect[1])
    #         self.rect[0] -= self.speed
    #         print('player - ', self.rect)
    #         # self.draw_player('left', self.screen)
    #     elif directory_of_movement == 'up':
    #         self.image.get_rect().move(self.rect[0], self.rect[1] - self.speed)
    #         self.rect[1] -= self.speed
    #         print('player - ', self.rect)
    #         # self.draw_player('up', self.screen)
    #     elif directory_of_movement == 'down':
    #         self.image.get_rect().move(self.rect[0], self.rect[1] + self.speed)
    #         self.rect[1] += self.speed
    #         print('player - ', self.rect)
    #         # self.draw_player('down', self.screen)
    #     else:
    #         print('staying')
    #
    #     self.update()
    #     pygame.display.update()
    #     pygame.display.flip()

    # draw
    def draw_player(self, directory_of_movement):
        print('draw_player')

        if self.frame + 1 > 30:
            self.frame = 0

        if directory_of_movement == 'left':
            self.cur_frame = self.frame // 5
            self.image = animation_left[self.cur_frame]
            self.screen.blit(self.image, (self.rect[0], self.rect[1]))
            self.frame += 1
            self.rect[0] -= self.speed
        elif directory_of_movement == 'right':
            self.cur_frame = self.frame // 5
            self.image = animation_right[self.cur_frame]
            self.screen.blit(self.image, (self.rect[0], self.rect[1]))
            self.frame += 1
            self.rect[0] += self.speed
        elif directory_of_movement == 'up':
            self.cur_frame = self.frame // 5
            self.image = animation_up[self.cur_frame]
            self.screen.blit(self.image, (self.rect[0], self.rect[1]))
            self.frame += 1
            self.rect[1] -= self.speed
        elif directory_of_movement == 'down':
            self.cur_frame = self.frame // 5
            self.image = animation_down[self.cur_frame]
            self.screen.blit(self.image, (self.rect[0], self.rect[1]))
            self.frame += 1
            self.rect[1] += self.speed
        else:
            self.screen.blit(animation_down[0], (self.rect[0], self.rect[1]))

        self.update()
        pygame.display.flip()

    def possibility_move(self, directory_of_movement, group):
        if directory_of_movement == 'right':
            tester = Player(self.speed, self.rect[0] + self.speed, self.rect[1], self.screen)
        elif directory_of_movement == 'left':
            tester = Player(self.speed, self.rect[0] - self.speed, self.rect[1], self.screen)
        elif directory_of_movement == 'up':
            tester = Player(self.speed, self.rect[1] - self.speed, self.rect[0], self.screen)
        else:
            tester = Player(self.speed, self.rect[1] + self.speed, self.rect[0], self.screen)

        if pygame.sprite.spritecollideany(tester, group):
            print('collision')
            tester.kill()
            return False
        else:
            return True

    # def update(self):
    #     self.rect = self.image.get_rect().move(self.rect[0] + self.speed, self.rect[1] + self.speed)
