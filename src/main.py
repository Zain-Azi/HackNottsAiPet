import pygame

from window import Window

window = Window("Hacknotts pet", 800, 600)
exit = False

while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
    pygame.display.update()