import pygame

class SpeechBubble:
    def __init__(self, text="", font_size=20, text_color=(0,0,0),
                 bubble_color=(255,255,255), outline_color=(0,0,0), corner_radius=15):
        self.font = pygame.font.SysFont("Papyrus", font_size)
        self.text = text
        text_width, text_height = self.font.size(self.text)
        if text_width > 1100:
            charW = self.font.size("M")[0]
            n = 1100 // charW  
            num_lines = (len(self.text) // n) + 1
            height = num_lines * self.font.get_height() + 20
            rect_x = (1280 - 1100) // 2
            self.rect = pygame.Rect(rect_x, 80, 1100, (height/2) + 30)
        else:
            rect_x = (1280 - text_width) // 2
            self.rect = pygame.Rect(rect_x, 80, text_width + 50, text_height + 20)
        
        self.text_color = text_color
        self.bubble_color = bubble_color
        self.outline_color = outline_color
        self.corner_radius = corner_radius

    def draw(self, screen):
        pygame.draw.rect(screen, self.bubble_color, self.rect, border_radius=self.corner_radius)
        tail = [(self.rect.centerx - 20, self.rect.bottom),
                (self.rect.centerx + 20, self.rect.bottom),
                (self.rect.centerx, self.rect.bottom + 20)]
        pygame.draw.polygon(screen, self.bubble_color, tail)

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
