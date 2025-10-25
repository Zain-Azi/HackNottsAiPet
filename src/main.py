import pygame

from dragon import Dragon
from speechbubble import SpeechBubble
from textbox import TextBox
from window import Window

window_w = 1280
window_h = 720

textbox_w = 1100
textbox_h = 60
textbox_x = (window_w - textbox_w) // 2
textbox_y = window_h - textbox_h - 20

clock = pygame.time.Clock()
FPS = 3

dragon = Dragon("Cheppie")

window = Window("Cheppie the Dragon", window_w, window_h)
textbox = TextBox(textbox_x, textbox_y, textbox_w, textbox_h)
bubble = SpeechBubble(500, 80, 300, 100, text="Hello, I am "+ dragon.get_name()+"!")

exit = False

sprite_value = 0

while not exit:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit = True
            
            if event.key == pygame.K_a:
                dragon.set_mood("angry")
            if event.key == pygame.K_h:
                dragon.set_mood("happy")
            if event.key == pygame.K_s:
                dragon.set_mood("sad")
            if event.key == pygame.K_n:
                dragon.set_mood("neutral")

        result = textbox.handle_event(event)
        if result is not None:
            user_input = result
            if user_input == "hello":
                bubble = SpeechBubble(500, 300, 300, 100, text="wagwan")
            else:
                bubble = SpeechBubble(500, 300, 300, 100, text="ok then...")
            
    sprite_value = (sprite_value + 1) % 2
    dragon.change_health(-10)

    window.update(sprite_value + 1, dragon.get_mood(), dragon.get_health())
    textbox.draw(window._Window__screen)
    bubble.draw(window._Window__screen)
    pygame.display.update()