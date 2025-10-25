import pygame

from textbox import TextBox
from window import Window
from speechbubble import SpeechBubble

window_w = 1280
window_h = 720

textbox_w = 1100
textbox_h = 60
textbox_x = (window_w - textbox_w) // 2
textbox_y = window_h - textbox_h - 20
window = Window("Cheppie the Dragon", window_w, window_h)
textbox = TextBox(textbox_x, textbox_y, textbox_w, textbox_h)
bubble = SpeechBubble(500, 300, 300, 100, text="Hello, I am Cheppie!")

exit = False

while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True

        result = textbox.handle_event(event)
        if result is not None:
            user_input = result
            if user_input == "hello":
                bubble = SpeechBubble(500, 300, 300, 100, text="wagwan")
            else:
                bubble = SpeechBubble(500, 300, 300, 100, text="ok then...")
            

    window.update()
    textbox.draw(window._Window__screen)
    bubble.draw(window._Window__screen)
    pygame.display.update()