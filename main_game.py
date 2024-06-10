def start_game():
    import pygame
    import random
    from buttons import ImageButton
    from main import Explosion


    explosion_anim_bottle = []
    for i in range(6):
        filename = f'{i}.png'
        img = pygame.image.load(f'img/boom_bottle/{filename}').convert()
        img.set_colorkey((255, 255, 255))
        img_lg = pygame.transform.scale(img, (75, 75))
        explosion_anim_bottle.append(img_lg)
    mirror_sound = pygame.mixer.Sound('sound/mirror.mp3')

    class Fruits_MENU(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((50, 50))
            self.image = pygame.image.load(f'img/products/{random.randint(1, 20)}.png')
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
        def __init__(self, x, y, name_fruit, size=65, low_pos=False, flag_rotate=False):
            pygame.sprite.Sprite.__init__(self)
            self.flag_rotate = flag_rotate
            self.x = x
            self.y = y
            self.size = size
            self.name_fruit = name_fruit.lower()  # курица
            self.get_img()
            self.clicked = False
            self.low_pos = low_pos  # попал ли фрукт в корзину
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
                            'пончик': 'img/products/8.png',
                            'пицца': 'img/products/9.png',
                            'яйцо': 'img/products/10.png',
                            'пирог': 'img/products/11.png',
                            'морковь': 'img/products/12.png',
                            'шоколад': 'img/products/13.png',
                            'мороженое': 'img/products/14.png',
                            'авокадо': 'img/products/15.png',
                            'хотдог': 'img/products/16.png',
                            'газировка': 'img/products/17.png',
                            'брокколи': 'img/products/18.png',
                            'клубника': 'img/products/19.png',
                            'банан': 'img/products/20.png',
                            }

            self.image = pygame.Surface((self.size, self.size))
            self.image = pygame.image.load(product_dict[self.name_fruit])
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
            self.image.set_colorkey((255, 255, 255))
            self.rect = self.image.get_rect()
            self.rect.bottom = self.y
            self.rect.centerx = self.x
            self.copy_y = self.rect.y

        def update(self):
            if self.clicked and self.flag_rotate:
                self.kill()
                for i in bottles:
                    if i.name == self.name_fruit: # нажали на продукт -> удаляем его и банку, перепещаем продукт в корзину

                        i.kill()
                        xxxxxx = Explosion(i.rect.center, explosion_anim_bottle)
                        mirror_sound.play()
                        bottle_boom.add(xxxxxx)
                        if len(shopping_bag) < 2:
                            shopping_bag.add(Fruits_For_Game(50 * len(shopping_bag) + 100, 670, i.name, 40, flag_rotate=True))
                        elif len(shopping_bag) < 6:
                            #test_windows.add(CancelWindow('img/prew.png'))
                            shopping_bag.add(Fruits_For_Game(50 * len(shopping_bag) - 50, 620, i.name, 40, flag_rotate=True))
                        else:
                            shopping_bag.add(Fruits_For_Game(50 * len(shopping_bag) - 200, 570, i.name, 40, flag_rotate=True))
                        if i.name in r_p.memory_products:
                            return 'yes'
                        elif i.name in r_p.extra_products:
                            return 'no'
                        elif i.name in r_p.killer_product:
                            return 'kill'
                            #score += 100
                print(self.name_fruit)

                #self.clicked = False
                #self.low_pos = True
            if self.low_pos:
                self.rotate()
            if self.flag_rotate:
                self.rotate()

        def play_sound(self):
            pass

        def handle_click(self, mouse_pos):
            if self.rect.collidepoint(mouse_pos):
                self.clicked = True
                self.play_sound()


    # Fruits_For_Game
    class DialogWindow(pygame.sprite.Sprite):
        def __init__(self, list_fruits: list[str],
                     killer_fruit: str,
                     path_img=None,
                     time=5):
            pygame.sprite.Sprite.__init__(self)
            self.list_fruits = list_fruits
            self.killer_fruit = killer_fruit
            self.time = time * 1000
            if not path_img:
                img = pygame.image.load(f'img/mem.png').convert()
            else:
                img = pygame.image.load(path_img).convert()
            img.set_colorkey((0, 0, 0))
            img = pygame.transform.scale(img, (1000, 700))
            self.image = img
            self.rect = self.image.get_rect(topleft=(0, 0))
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
                fruits_memory.add(Fruits_For_Game((i + 1) * 130 + 200, 350, first_line[i], size=100))
            for i in range(len(second_line)):
                fruits_memory.add(Fruits_For_Game((i + 1) * 130 + 200, 500, second_line[i], size=100))
            fruits_memory.add(Fruits_For_Game(870, 650, self.killer_fruit, size=120))

        def update(self):
            self.font = pygame.font.Font('font/agat-8.ttf', 60)
            now = pygame.time.get_ticks()
            text = self.font.render(str(round((self.time - (now - self.last_update)) / 1000, 2)), True, (255, 0, 0))
            screen.blit(text, (60, 120))
            if now - self.last_update > self.time:
                for i in fruits_memory:
                    i.kill()
                self.kill()

                '''
                1    2    3    4   5   6
                7    8    9   10  11  12
                13  13   15   16  17  18
                '''

                # установить банки
                r_p.put_bottle()


    class CancelWindow(pygame.sprite.Sprite):
        def __init__(self, img, text='', btn_text='ok', ):
            pygame.sprite.Sprite.__init__(self)
            self.text = text
            self.btn_text = btn_text
            self.image = pygame.Surface((1000, 700))
            self.image = pygame.image.load(img)
            self.image = pygame.transform.scale(self.image, (1000, 700))
            self.image.set_colorkey((255, 255, 255))
            self.rect = self.image.get_rect()
            self.rect.bottom = WIDTH // 2 - 300
            self.rect.centerx = HEIGHT // 2 - 200

            self.rect = self.image.get_rect(topleft=(0, 0))
            self.clicked = False



        def handle_click(self, mouse_pos):
            if self.rect.collidepoint(mouse_pos):
                self.clicked = True


        def update(self):
            self.font = pygame.font.Font('font/agat-8.ttf', 40)
            text = self.font.render(self.text, True, (255, 255, 255))
            screen.blit(text, (420, 180))
            if self.clicked:
                r_p.put_memory()
                self.kill()

    class Bottle(pygame.sprite.Sprite):
        def __init__(self, x, y, name):
            pygame.sprite.Sprite.__init__(self)
            self.x = x
            self.y = y
            self.name = name # имя банки = имени продукта в ней
            self.image = pygame.Surface((1000, 700))
            self.image = pygame.image.load('img/bottle.png')
            self.image = pygame.transform.scale(self.image, (110, 110))
            self.image.set_colorkey((255, 255, 255))
            self.rect = self.image.get_rect()
            self.rect.centery = self.y
            self.rect.centerx = self.x


        def update(self):
            pass







    def settings_game():
        d = {}
        with open('settings.txt', 'r') as file:
            for i in file:
                x = i.split('=')
                key, value = x[0], int(x[1])
                d[key] = value
        return d





    class Random_Products:
        def __init__(self, round=1):
            self.round = round
            self.settings = settings_game()
            self.all_products = ['сыр', 'курица', 'баклажан', 'груша', 'перец', 'рыба', 'лимон', 'пончик', 'пицца', 'яйцо', 'пирог', 'морковь', 'шоколад', 'мороженое', 'авокадо', 'хотдог', 'газировка', 'брокколи', 'клубника', 'банан']
            self.get_random_product_for_memory()
            self.get_extra_products()


        def get_random_product_for_memory(self):
            '''  получить список продуктов, которые нужно запомнить

            :return:
            '''

            copy_list = self.all_products[:]
            random.shuffle(copy_list)
            self.amount_products_memory = min(8, self.settings['products_memory'] + self.round - 1) # число продуктов для запоминания не больше 8
            self.memory_products = copy_list[:self.amount_products_memory]
            self.get_killer_product()


        def get_extra_products(self):
            '''  получить список продуктов, которые нельзя выбирать

            :return:
            '''

            extra_products = list(set(self.all_products) - set(self.memory_products)) # продукты которые остались
            random.shuffle(extra_products)
            self.amount_extra_products = min(self.round * 3, 18 - self.amount_products_memory) # количество лишних продуктов
            self.extra_products = extra_products[:self.amount_extra_products]


        def get_killer_product(self):
            self.killer_product = random.choice(list(set(self.all_products) - set(self.memory_products))) # продукт-убийца


        def put_bottle(self):
            '''  поставить банки с едой на случайные месат

            :return:
            '''


            position_bottles_and_products = [[250, 156, 200],
                                             [375, 156, 200],
                                             [510, 156, 200],
                                             [610, 156, 200],
                                             [710, 156, 200],
                                             [810, 156, 200],

                                             [250, 287, 328],
                                             [375, 287, 328],
                                             [510, 287, 328],
                                             [610, 287, 328],
                                             [710, 287, 328],
                                             [810, 287, 328],

                                             [250, 471, 512],
                                             [375, 471, 512],
                                             [510, 471, 512],
                                             [610, 471, 512],
                                             [710, 471, 512],
                                             [810, 471, 512],
                                             ]

            random_index = [i for i in range(18)]
            random.shuffle(random_index)
            products_screen = self.memory_products + self.extra_products + [self.killer_product] # продукты которые будут на экране
            random.shuffle(products_screen)

            counter = 0
            for i in random_index[:self.amount_extra_products + self.amount_products_memory + 1]:
                bottles.add(Bottle(position_bottles_and_products[i][0], position_bottles_and_products[i][1], products_screen[counter]))
                fruits_memory.add(Fruits_For_Game(position_bottles_and_products[i][0], position_bottles_and_products[i][2], products_screen[counter], flag_rotate=True))
                counter += 1


            for i in random_index[self.amount_extra_products + self.amount_products_memory:]:
                bottles.add(Bottle(position_bottles_and_products[i][0], position_bottles_and_products[i][1], 'None'))



        def put_memory(self):
            '''

            :return:
            '''
            d_win.add(DialogWindow(self.memory_products, self.killer_product, time=self.settings['time']))





    WIDTH = 1000  # ширина игрового окна
    HEIGHT = 700  # высота игрового окна
    FPS = 60  # частота кадров в секунду
    main_bg = pygame.image.load('img/shop1.png')

    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Shop")
    clock = pygame.time.Clock()
    fruits_memory = pygame.sprite.Group()
    d_win = pygame.sprite.Group()
    draw_mem = False
    bottle_boom = pygame.sprite.Group()
    test_windows = pygame.sprite.Group()
    test_windows.add(CancelWindow('img/prew.png'))

    bottles = pygame.sprite.Group()
    round_number = 1
    r_p = Random_Products(round_number)
    # r_p.put_memory()
    highscore_main = r_p.settings['record']
    shopping_bag = pygame.sprite.Group()
    score = 0

    def clear_screen():
        for i in shopping_bag:
            i.kill()

        for i in bottles:
            i.kill()

        for i in fruits_memory:
            i.kill()






    count_memory = 0 # сколько отгадали за раунд
    running = True
    while running:
        clock.tick(FPS)
        screen.fill((0, 0, 0))
        screen.blit(main_bg, (0, 0))
        font = pygame.font.Font('font/agat-8.ttf', 60)
        text_surface = font.render(f'health {score}', True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH / 2, 30))


        f_rec = pygame.font.Font('font/agat-8.ttf', 20)
        text_rec = f_rec.render(f'highscore: {highscore_main}', True, (255, 255, 255))
        text_rec_rect = text_rec.get_rect(center=(100, 30))
        screen.blit(text_rec, text_rec_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for k in test_windows:
                        k.handle_click(pygame.mouse.get_pos())
                    for xx in fruits_memory:
                        xx.handle_click(pygame.mouse.get_pos())

        screen.blit(text_surface, text_rect)
        test_windows.draw(screen)
        test_windows.update()

        bottles.draw(screen)
        bottles.update()


        d_win.draw(screen)
        fruits_memory.draw(screen)
        d_win.update()
        #fruits_memory.update()
        for i in fruits_memory:
            res_update = i.update()
            if res_update == 'yes':
                count_memory += 1
                score += 100
                if score > highscore_main:
                    highscore_main = score
                    r_p.settings['record'] = highscore_main
                    with open('settings.txt', 'w') as file:
                        for key, value in r_p.settings.items():
                            print(f'{key}={value}', file=file)
                    file.close()

                if r_p.amount_products_memory == count_memory:
                    clear_screen()
                    count_memory = 0
                    round_number += 1
                    test_windows.add(CancelWindow('img/r_win.png', text=f'раунд: {round_number}'))  # тут лого победы

                    r_p = Random_Products(round_number)
            elif res_update == 'no':

                score -= 200
                if score < 0:
                    clear_screen()
                    score = 0
                    count_memory = 0
                    test_windows.add(CancelWindow('img/loose.png'), )  # тут лого смерти
            elif res_update == 'kill':
                clear_screen()
                score = 0
                count_memory = 0
                test_windows.add(CancelWindow('img/loose.png'))  # тут лого смерти


        bottle_boom.draw(screen)
        bottle_boom.update()

        shopping_bag.draw(screen)
        shopping_bag.update()

        pygame.display.flip()


