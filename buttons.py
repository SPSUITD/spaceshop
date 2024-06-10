import pygame

# класс кнопки с картинкой
class ImageButton:
    def __init__(self,
                 x, y,
                 width,
                 height,
                 text,
                 image_path,
                 hover_img_path=None,
                 sound_path=None,
                 opacity=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.image = pygame.image.load(image_path)
        self.image.set_colorkey((255, 255, 255))
        if opacity:
            self.image.set_alpha(200)  # прозрачность
        self.image = pygame.transform.scale(self.image, (width, height))
        self.hover_img_path = self.image


        if hover_img_path:
            self.hover_image = pygame.image.load(hover_img_path)
            self.hover_image.set_colorkey((255, 255, 255))
            self.hover_image = pygame.transform.scale(self.hover_image, (width, height))
        else:
            self.hover_image = self.image
            self.hover_image.set_colorkey((255, 255, 255))

        self.rect = self.image.get_rect(topleft=(x, y))
        self.sound = None

        if sound_path:
            self.sound = pygame.mixer.Sound(sound_path)
        self.is_hovered = False

    def draw(self, screen):
        if self.is_hovered:
            current_image = self.hover_image
        else:
            current_image = self.image

        screen.blit(current_image, self.rect.topleft)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            if self.sound:
                self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))




