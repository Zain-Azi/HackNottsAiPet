import pygame

class SpeechBubble:
    def __init__(self, x, y, w, h, text="", font_size=24, text_color=(0,0,0),
                 bubble_color=(255,255,255), outline_color=(0,0,0), corner_radius=15):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = pygame.font.SysFont("Papyrus", font_size)
        self.text_color = text_color
        self.bubble_color = bubble_color
        self.outline_color = outline_color
        self.corner_radius = corner_radius

    def draw(self, screen):
        pygame.draw.rect(screen, self.bubble_color, self.rect, border_radius=self.corner_radius)
        tail = [(self.rect.centerx - 100, self.rect.bottom),
                (self.rect.centerx - 60, self.rect.bottom),
                (self.rect.centerx - 90, self.rect.bottom + 20)]
        pygame.draw.polygon(screen, self.bubble_color, tail)

        # Draw text (wrap if needed)
        self.draw_text(screen)

    def draw_text(self, screen):
        words = self.text.split(' ')
        lines = []
        line = ""
        for word in words:
            test_line = line + word + " "
            if self.font.size(test_line)[0] < self.rect.width - 20:  # padding
                line = test_line
            else:
                lines.append(line)
                line = word + " "
        lines.append(line)

        for i, line in enumerate(lines):
            text_surf = self.font.render(line, True, self.text_color)
            screen.blit(text_surf, (self.rect.x + 10, self.rect.y + 10 + i * self.font.get_height()))
