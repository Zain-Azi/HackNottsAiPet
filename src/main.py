import pygame

from window import Window
from textbox import TextBox

window_w = 1280
window_h = 720

textbox_w = 1100
textbox_h = 60
textbox_x = (window_w - textbox_w) // 2  # centers horizontally
textbox_y = window_h - textbox_h - 20  # 20 px margin from bottom

window = Window("Cheppie the Dragon", window_w, window_h)
textbox = TextBox(textbox_x, textbox_y, textbox_w, textbox_h)

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