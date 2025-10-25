import pygame

class TextBox:
    def __init__(self, x, y, w, h, font_size=24, text_color=(0,0,0), box_color=(255,255,255)):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = box_color
        self.text_color = text_color
        self.font = pygame.font.Font(None, font_size)
        self.text = ""
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                entered_text = self.text
                self.text = ""
                return entered_text
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
        return None

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        txt_surface = self.font.render(self.text, True, self.text_color)
        screen.blit(txt_surface, (self.rect.x+5, self.rect.y+5))
        if self.active:
            pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)