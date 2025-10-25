import pygame


class Window:
    def __init__(self, title, width, height):
        self.title = title
        self.WIDTH = width
        self.HEIGHT = height

        pygame.init()
        self.__screen=pygame.display.set_mode((width,height),pygame.SRCALPHA)
        pygame.display.set_caption(title)

    def resize(self, width, height):
        self.width = width
        self.height = height

    def get_size(self):
        return self.width, self.height

    def set_title(self, title):
        self.title = title

    def get_title(self):
        return self.title