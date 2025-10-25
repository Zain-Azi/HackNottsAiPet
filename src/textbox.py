import pygame

class TextBox:
    def __init__(self, x, y, w, h, font_size=24, font_name=None, text_color=(50,50,50),
                 box_color=(255,255,255), outline_color=(0,0,0), outline_thickness=3,
                 corner_radius=15, placeholder="Speak to your pet", send_button=True):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = box_color
        self.text_color = text_color
        self.outline_color = outline_color
        self.outline_thickness = outline_thickness
        self.corner_radius = corner_radius
        self.placeholder = placeholder
        self.active = False
        self.text = ""

        if font_name:
            self.font = pygame.font.SysFont("Comic Sans MS", font_size)
        else:
            self.font = pygame.font.SysFont("Comic Sans MS", font_size)

        self.send_button_enabled = send_button
        if self.send_button_enabled:
            self.button_width = 80
            self.button_height = h
            self.button_rect = pygame.Rect(x + w - 80, y, self.button_width, self.button_height)
            self.button_color = (79, 0, 0)
            self.button_text_color = (255, 255, 255)
            self.button_font = pygame.font.SysFont("Comic Sans MS", font_size)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

            if self.send_button_enabled and self.button_rect.collidepoint(event.pos):
                entered_text = self.text
                self.text = ""
                return entered_text

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
        pygame.draw.rect(screen, self.color, self.rect, border_radius=self.corner_radius)
        pygame.draw.rect(screen, self.outline_color, self.rect, width=self.outline_thickness, border_radius=self.corner_radius)

        display_text = self.text if self.text else self.placeholder
        text_surf = self.font.render(display_text, True, self.text_color)
        screen.blit(text_surf, (self.rect.x + 10, self.rect.y + (self.rect.height - text_surf.get_height()) // 2))
        if self.send_button_enabled:
            pygame.draw.rect(screen, self.button_color, self.button_rect, border_radius=10)
            pygame.draw.rect(screen, self.outline_color, self.button_rect, width=2, border_radius=10)
            btn_text = self.button_font.render("Send", True, self.button_text_color)
            screen.blit(btn_text, (self.button_rect.x + (self.button_width - btn_text.get_width())//2,
                                   self.button_rect.y + (self.button_height - btn_text.get_height())//2))
