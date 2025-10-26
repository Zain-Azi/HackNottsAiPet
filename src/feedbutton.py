import pygame


class FeedButton:
    def __init__(self, x, y, w, h, text="Feed", box_color=(200, 200, 200), text_color=(0, 0, 0),
                 outline_color=(0, 0, 0), outline_thickness=2, corner_radius=10,
                 font_size=24, font_name=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = box_color
        self.text_color = text_color
        self.outline_color = outline_color
        self.outline_thickness = outline_thickness
        self.corner_radius = corner_radius
        self.text = text

        if font_name:
            self.font = pygame.font.SysFont(font_name, font_size)
        else:
            self.font = pygame.font.SysFont("Comic Sans MS", font_size)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=self.corner_radius)
        pygame.draw.rect(screen, self.outline_color, self.rect, width=self.outline_thickness,
                         border_radius=self.corner_radius)

        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)