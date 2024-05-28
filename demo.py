import pygame
import random


class Fruits_MENU(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image = pygame.image.load(f'img/products/{random.randint(1, 19)}.png')
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -4
        self.last_update = pygame.time.get_ticks()
        self.rot = 0
        self.rot_speed = random.randrange(-12, 12)
        self.image_orig = self.image.copy()
        self.is_hovered = False

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)


class Fruits_For_Game(pygame.sprite.Sprite):
    def __init__(self, x, y, name_fruit, size=70, low_pos=False):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.size = size
        self.name_fruit = name_fruit.lower() # курица
        self.get_img()
        self.clicked = False
        self.low_pos = low_pos # попал ли фрукт в корзину
        self.last_update = pygame.time.get_ticks()
        self.rot = 0
        self.rot_speed = random.choice([-4, -5, -6, -7, -8, -9, 4, 5, 6, 7, 8, 9])
        self.image_orig = self.image.copy()


    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def get_img(self):

        product_dict = {'сыр': 'img/products/1.png',
                        'курица': 'img/products/2.png',
                        'баклажан': 'img/products/3.png',
                        'груша': 'img/products/4.png',
                        'перец': 'img/products/5.png',
                        'рыба': 'img/products/6.png',
                        'лимон': 'img/products/7.png',
                        'пончик': 'img/products/8.png'}

        self.image = pygame.Surface((self.size, self.size))
        self.image = pygame.image.load(product_dict[self.name_fruit])
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.bottom = self.y
        self.rect.centerx = self.x
        self.copy_y = self.rect.y


    def update(self):
        if self.clicked:
            print(self.name_fruit)
            self.clicked = False
            self.low_pos = True
        elif self.low_pos:
            self.rotate()



    def play_sound(self):
        pass

    def handle_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.clicked = True
            self.play_sound()


#Fruits_For_Game
class DialogWindow(pygame.sprite.Sprite):
    def __init__(self, list_fruits: list[str],
                 favorite_fruit: str,
                 killer_fruit: str,
                 path_img=None,
                 time=5):
        pygame.sprite.Sprite.__init__(self)
        self.list_fruits = list_fruits
        self.killer_fruit = killer_fruit
        self.time = time * 1000
        self.favorite_fruit = favorite_fruit
        if not path_img:
            img = pygame.image.load(f'img/bg_menu.png').convert()
        else:
            img = pygame.image.load(path_img).convert()
        img.set_colorkey((0, 0, 0))
        img = pygame.transform.scale(img, (600, 400))
        self.image = img
        self.rect = self.image.get_rect(topleft=(WIDTH // 2 - 300, HEIGHT // 2 - 200))
        self.last_update = pygame.time.get_ticks()
        self.get_fruits()

    def get_fruits(self):
        if len(self.list_fruits) % 2 == 0:
            first_line = self.list_fruits[:len(self.list_fruits) // 2]
            second_line = self.list_fruits[len(self.list_fruits) // 2:]
        else:
            first_line = self.list_fruits[:len(self.list_fruits) // 2 + 1]
            second_line = self.list_fruits[len(self.list_fruits) // 2 + 1:]

        for i in range(len(first_line)):
            fruits_memory.add(Fruits_For_Game((i + 1) * 100 + 150, 350, first_line[i]))
        for i in range(len(second_line)):
            fruits_memory.add(Fruits_For_Game((i + 1) * 100 + 150, 450, second_line[i]))
        fruits_memory.add(Fruits_For_Game(750, 350, self.favorite_fruit, size=40))

    def update(self):
        self.font = pygame.font.SysFont(None, 50)
        now = pygame.time.get_ticks()
        text = self.font.render(str(round((self.time - (now - self.last_update)) / 1000, 2)), True, (0, 0, 0))
        screen.blit(text, (300, 300))
        if now - self.last_update > self.time:
            for i in fruits_memory:
                i.kill()
            self.kill()






if __name__ == "__main__":

    WIDTH = 1000  # ширина игрового окна
    HEIGHT = 700 # высота игрового окна
    FPS = 60 # частота кадров в секунду
    main_bg = pygame.image.load('img/main_menu.png')



    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Shop")
    clock = pygame.time.Clock()
    fruits_memory = pygame.sprite.Group()
    d_win = pygame.sprite.Group()
    d_win.add(DialogWindow(['сыр', 'рыба', 'перец'], 'сыр', 'сыр', time=10))



    running = True
    while running:
        clock.tick(FPS)
        screen.fill((0, 0, 0))
        screen.blit(main_bg, (0, 0))
        font = pygame.font.Font(None, 80)
        text_surface = font.render('тест', True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH / 2, 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for xx in fruits_memory:
                        xx.handle_click(pygame.mouse.get_pos())

        d_win.draw(screen)
        fruits_memory.draw(screen)
        d_win.update()
        fruits_memory.update()



        screen.blit(text_surface, text_rect)
        pygame.display.flip()





# WIDTH = 1000  # ширина игрового окна
# HEIGHT = 700 # высота игрового окна
# FPS = 60 # частота кадров в секунду
# main_bg = pygame.image.load('img/main_menu.png')
#
#
#
# pygame.init()
# pygame.mixer.init()
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Space Shop")
# clock = pygame.time.Clock()
#
# fruits_memory = pygame.sprite.Group()
# for i in range(7):
#     f = Fruits_MENU(random.randint(0, WIDTH), random.randint(0, HEIGHT))
#     fruits_memory.add(f)
#
# running = True
# while running:
#     clock.tick(FPS)
#     screen.fill((0, 0, 0))
#     screen.blit(main_bg, (0, 0))
#     font = pygame.font.Font(None, 80)
#     text_surface = font.render('SPACE SHOP', True, (255, 255, 255))
#     text_rect = text_surface.get_rect(center=(WIDTH / 2, 100))
#
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
#     fruits_memory.draw(screen)
#     fruits_memory.update()
#
#     if len(fruits_memory) < 10:
#         for __ in range(7 - len(fruits_memory)):
#             fruits_memory.add(Fruits_MENU(random.randint(0, WIDTH), HEIGHT + 100))
#
#     screen.blit(text_surface, text_rect)
#     pygame.display.flip()
