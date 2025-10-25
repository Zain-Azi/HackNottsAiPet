import pygame


class Window:
    def __init__(self, title, width, height):
        self.title = title
        self.WIDTH = width
        self.HEIGHT = height

        pygame.init()
        self.__screen=pygame.display.set_mode((width,height),pygame.SRCALPHA)
        pygame.display.set_caption(title)

        self.__images = {
            "background": pygame.image.load("assets/background.png").convert(),
            "neutral1": pygame.image.load("assets/idle1.png").convert_alpha(),
            "neutral2": pygame.image.load("assets/idle2.png").convert_alpha(),
            "happy1": pygame.image.load("assets/happy1.png").convert_alpha(),
            "happy2": pygame.image.load("assets/happy2.png").convert_alpha(),
            "sad1": pygame.image.load("assets/sad1.png").convert_alpha(),
            "sad2": pygame.image.load("assets/sad2.png").convert_alpha(),
            "angry1": pygame.image.load("assets/angry1.png").convert_alpha(),
            "angry2": pygame.image.load("assets/angry2.png").convert_alpha()
        }

    def update(self, counter, mood, hp):
        bg = pygame.transform.scale(self.__images["background"], (self.WIDTH, self.HEIGHT))
        self.__screen.blit(bg, (0, 0))
        self.__screen.blit(pygame.transform.scale(self.__images[mood+str(counter)], (400, 400)),
                        ((self.WIDTH - 400)/2, self.HEIGHT - 500))
        
        pygame.draw.rect(self.__screen, (107, 61, 5), (20, 40, 50, 510), border_radius=20, width=5)
        pygame.draw.rect(self.__screen, (0, 0, 0), (25, 45, 40, 500), border_radius=15)
        pygame.draw.rect(self.__screen, (4, 219, 8), (25, 45+(1000-hp)/2, 40, hp/2), border_radius=15)
        pygame.draw.rect(self.__screen, (107, 61, 5), (20, 40, 50, 510), border_radius=20, width=5)

    def resize(self, width, height):
        self.width = width
        self.height = height

    def get_size(self):
        return self.width, self.height

    def set_title(self, title):
        self.title = title

    def get_title(self):
        return self.title