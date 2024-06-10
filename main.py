from buttons import ImageButton
import warnings
import sys
import pygame
import random
from product_menu import Fruits_MENU
import time



def settings_game():
    d = {}
    with open('settings.txt', 'r') as file:
        for i in file:
            x = i.split('=')
            key, value = x[0], int(x[1])
            d[key] = value
    return d


pygame.init()
warnings.filterwarnings('ignore')

WIDTH, HEIGHT = 960, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('pixel shop')


main_bg = pygame.image.load('img/main_menu.jpg')


explosion_anim_menu = []
for i in range(9):
    filename = f'{i}.png'
    img = pygame.image.load(f'img/boom/{filename}').convert()
    img.set_colorkey((0, 0, 0))
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim_menu.append(img_lg)




class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, explosion_anim):

        pygame.sprite.Sprite.__init__(self)
        self.explosion_anim = explosion_anim
        self.image = self.explosion_anim[0]
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
            if self.frame == len(self.explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center




def main_menu():
    settings = settings_game()
    minigame_highscore = settings['record_minigame']
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
    enemy = pygame.sprite.Group() # бомбы
    score_minigame = 0
    secret_game = False
    running = True
    while running:
        clock.tick(FPS)
        screen.fill((0, 0, 0))
        screen.blit(main_bg, (0, 0))
        font = pygame.font.Font('font/agat-8.ttf', 80)
        text_surface = font.render('SPACE SHOP', True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH / 2, 100))


        if secret_game:
            font = pygame.font.Font('font/agat-8.ttf', 30)
            score_minigame_text = font.render(f'score: {score_minigame} record: {minigame_highscore}', True, (255, 255, 255))
            score_minigame_text_rect = score_minigame_text.get_rect(center=(WIDTH / 2, 160))
            screen.blit(score_minigame_text, score_minigame_text_rect)


        fruits.draw(screen)
        fruits.update()
        all_sprites.draw(screen)
        all_sprites.update()

        if len(fruits) < 10:
            for __ in range(7 - len(fruits)):
                fruits.add(Fruits_MENU(random.randint(0, WIDTH), HEIGHT + 100))

        screen.blit(text_surface, text_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.USEREVENT and event.button == close_btn:

                time.sleep(.5)
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == start_btn:
                game()

            if event.type == pygame.USEREVENT and event.button == settings_btn:
                setting_menu()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for j in fruits:
                        x, y = j.rect.center[0], j.rect.center[1]
                        x_mouse, y_mouse = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                        if abs(x - x_mouse) < 30 and abs(y - y_mouse) < 30:
                            j.kill()
                            expl = Explosion(j.rect.center, explosion_anim_menu)
                            all_sprites.add(expl)
                            score_minigame += 100
                            if score_minigame > minigame_highscore:
                                minigame_highscore = score_minigame
                                settings['record_minigame'] = minigame_highscore
                                with open('settings.txt', 'w') as file:
                                    for key, value in settings.items():
                                        print(f'{key}={value}', file=file)
                                file.close()



                            if score_minigame > 0:
                                secret_game = True

                            if score_minigame >= 300:
                                for i in range(score_minigame // 300):
                                    enemy.add(Fruits_MENU(random.randint(50, 950), random.randint(0, HEIGHT), True))
                            boom_sound.play()
                            break
                    for j in enemy: # ударили бoмбу в главном меню
                        x, y = j.rect.center[0], j.rect.center[1]
                        x_mouse, y_mouse = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                        if abs(x - x_mouse) < 30 and abs(y - y_mouse) < 30:
                            j.kill()
                            expl = Explosion(j.rect.center, explosion_anim_menu)
                            all_sprites.add(expl)
                            score_minigame = 0
                            boom_sound.play()


            for btn in [settings_btn, start_btn, close_btn]:
                btn.handle_event(event)

        enemy.draw(screen)
        enemy.update()

        for btn in [settings_btn, start_btn, close_btn]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)




        pygame.display.flip()


def setting_menu():
    from slider_settings import Slider


    def change_settings():
        settings['time'] = slider_time_mem.value
        settings['products_memory'] = slider_mem_product.value
        settings['extra_products'] = slider_extra_product.value
        with open('settings.txt', 'w') as file:
            for i, j in settings.items():
                print(f'{i}={j}', file=file)
        file.close()

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    settings = settings_game()
    slider_mem_product = Slider(370, 165, 200, 40, (247, 94, 94), (39, 145, 31), 1, 8)
    slider_extra_product = Slider(370, 260, 200, 40, (247, 94, 94), (39, 145, 31), 1, 12)
    slider_time_mem = Slider(370, 345, 200, 40, (247, 94, 94), (39, 145, 31), 1, 10)
    slider_time_mem.set_value(settings['time'])
    slider_mem_product.set_value(settings['products_memory'])
    slider_extra_product.set_value(settings['extra_products'])
    btn_save_exit = ImageButton(190, 500, 380, 60, 'СОХРАНИТЬ И ВЫЙТИ', 'img/save_exit.png',
                                sound_path='sound/test.mp3')

    settings_bg = pygame.image.load('img/settings.png')
    pygame.display.set_caption("Settings")
    r = True
    while r:
        screen.fill((255, 255, 255))
        screen.blit(settings_bg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == btn_save_exit:
                change_settings()
                r = False
                main_menu()

            btn_save_exit.handle_event(event)

            slider_mem_product.update(event)
            slider_extra_product.update(event)
            slider_time_mem.update(event)

        slider_mem_product.draw(screen)
        slider_extra_product.draw(screen)
        slider_time_mem.draw(screen)
        btn_save_exit.draw(screen)
        btn_save_exit.check_hover(pygame.mouse.get_pos())
        pygame.display.flip()
        clock.tick(60)


def game():
    from main_game import start_game
    start_game()


if __name__ == '__main__':
    main_menu()

