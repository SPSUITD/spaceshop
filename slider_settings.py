import pygame
import sys
# слайдер  для настроек напрмиер сложность или количество фруктов

class Slider:
    def __init__(self, x, y, width, height, slider_color, thumb_color, start_value, stop_value, step=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.slider_color = slider_color
        self.thumb_color = thumb_color
        self.start_value = start_value
        self.value = start_value
        self.stop_value = stop_value
        self.step = step
        
        self.font = pygame.font.SysFont('Arial', 24)

        self.thumb_width = 16
        self.thumb_height = height
        self.thumb_x = self.x
        self.thumb_y = self.y

        self.dragging = False

    def draw(self, screen):
        # Draw slider bar
        pygame.draw.rect(screen, self.slider_color, (self.x, self.y, self.width, self.height))

        pygame.draw.rect(screen, self.thumb_color, (self.thumb_x, self.thumb_y, self.thumb_width, self.thumb_height))


        text = self.font.render(str(self.value), True, (255, 0, 0))
        screen.blit(text, (self.x + self.width // 2 - text.get_width() // 2, self.y - 30))

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.thumb_x <= mouse_pos[0] <= self.thumb_x + self.thumb_width and self.thumb_y <= mouse_pos[1] <= self.thumb_y + self.height:
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        if self.dragging:
            mouse_x, _ = pygame.mouse.get_pos()
            new_value = int((mouse_x - self.x) / self.width * (self.stop_value - self.start_value))
            self.value = max(self.start_value, min(self.stop_value, new_value))
            self.thumb_x = self.x + (self.value - self.start_value) / (self.stop_value - self.start_value) * self.width

#
# pygame.init()
# screen = pygame.display.set_mode((800, 600))
# clock = pygame.time.Clock()
#
# slider = Slider(100, 300, 200, 20, (100, 100, 100), (200, 200, 200), 0, 5)
#
# while True:
#     screen.fill((255, 255, 255))
#
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#
#         slider.update(event)
#
#     slider.draw(screen)
#
#     pygame.display.flip()
#     clock.tick(60)