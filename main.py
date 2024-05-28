from buttons import ImageButton

import sys
import pygame
import random
from demo import Fruits_MENU

pygame.init()

WIDTH, HEIGHT = 960, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('pixel shop')


main_bg = pygame.image.load('img/main_menu.jpg')


explosion_anim = []
for i in range(9):
    filename = f'{i}.png'
    img = pygame.image.load(f'img/boom/{filename}').convert()
    img.set_colorkey((0, 0, 0))
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim.append(img_lg)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):

        pygame.sprite.Sprite.__init__(self)
        self.image = explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center




def main_menu():
    boom_sound = pygame.mixer.Sound('sound/boom.mp3')
    WIDTH = 1000  # ширина игрового окна
    HEIGHT = 700  # высота игрового окна
    FPS = 60  # частота кадров в секунду
    main_bg = pygame.image.load('img/main_menu.png')

    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Shop")
    clock = pygame.time.Clock()

    fruits = pygame.sprite.Group()

    for i in range(7):
        f = Fruits_MENU(random.randint(0, WIDTH), random.randint(0, HEIGHT))
        fruits.add(f)

    start_btn = ImageButton(WIDTH/2-250/2, 200, 260, 70, 'играть', 'img/bg_menu.png', None, 'sound/test.mp3', True)
    settings_btn = ImageButton(WIDTH/2-250/2, 300, 260, 70, 'настройки', 'img/bg_menu.png', None, 'sound/test.mp3', True)
    close_btn = ImageButton(WIDTH/2-250/2, 400, 260, 70, 'выйти', 'img/bg_menu.png', None, 'sound/test.mp3', True)
    all_sprites = pygame.sprite.Group()
    running = True
    while running:
        clock.tick(FPS)
        screen.fill((0, 0, 0))
        screen.blit(main_bg, (0, 0))
        font = pygame.font.Font(None, 80)
        text_surface = font.render('SPACE SHOP', True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH / 2, 100))
        fruits.draw(screen)
        fruits.update()
        all_sprites.draw(screen)
        all_sprites.update()

        if len(fruits) < 10:
            for __ in range(7 - len(fruits)):
                fruits.add(Fruits_MENU(random.randint(0, WIDTH), HEIGHT + 100))

        screen.blit(text_surface, text_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for j in fruits:
                        x, y = j.rect.center[0], j.rect.center[1]
                        x_mouse, y_mouse = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                        if abs(x - x_mouse) < 30 and abs(y - y_mouse) < 30:
                            j.kill()
                            expl = Explosion(j.rect.center)
                            all_sprites.add(expl)
                            boom_sound.play()
                            break

            for btn in [settings_btn, start_btn, close_btn]:
                btn.handle_event(event)


        for btn in [settings_btn, start_btn, close_btn]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)




        pygame.display.flip()


def setting_menu():
    pass


def game():
    pass



if __name__ == '__main__':
    main_menu()

