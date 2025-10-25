import pygame

from window import Window
from textbox import TextBox

window = Window("Cheppie the Dragon", 800, 600)
textbox = TextBox(50, 550, 700, 40)

exit = False

while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True

        result = textbox.handle_event(event)
        if result is not None:
            user_input = result
            print(user_input)  

    textbox.draw(window._Window__screen)   
    pygame.display.update()