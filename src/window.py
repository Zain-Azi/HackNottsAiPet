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
            "background": pygame.image.load("assets/background_proto.png").convert(),
            "idle1": pygame.image.load("assets/idle1.JPEG").convert_alpha(),
            "idle2": pygame.image.load("assets/idle2.JPEG").convert_alpha(),
            "happy1": pygame.image.load("assets/happy1.JPEG").convert_alpha(),
            "happy2": pygame.image.load("assets/happy2.JPEG").convert_alpha(),
            "sad1": pygame.image.load("assets/sad1.JPEG").convert_alpha(),
            "sad2": pygame.image.load("assets/sad2.JPEG").convert_alpha(),
            "angry1": pygame.image.load("assets/angry1.JPEG").convert_alpha(),
            "angry2": pygame.image.load("assets/angry2.JPEG").convert_alpha()
        }

    def update(self):
        bg = pygame.transform.scale(self.__images["background"], (self.WIDTH, self.HEIGHT))
        self.__screen.blit(bg, (0, 0))
        self.__screen.blit(pygame.transform.scale(self.__images["idle1"], (400, 400)),
                        ((self.WIDTH - 400)/2, self.HEIGHT - 600))

    def resize(self, width, height):
        self.width = width
        self.height = height

    def get_size(self):
        return self.width, self.height

    def set_title(self, title):
        self.title = title

    def get_title(self):
        return self.title