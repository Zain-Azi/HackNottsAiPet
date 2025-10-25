import pygame

import emotion_react
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
FPS = 30

dragon = Dragon("Cheppie")

window = Window("Cheppie the Dragon", window_w, window_h)
textbox = TextBox(textbox_x, textbox_y, textbox_w, textbox_h)
bubble = SpeechBubble(text="Hello, I am "+ dragon.get_name()+"!")

exit = False

sprite_value = 0

last_anim_update = pygame.time.get_ticks()

while not exit:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit = True
            if event.key == pygame.K_f:
                dragon.set_action("breathe_fire")
            
        result = textbox.handle_event(event)
        if result is not None:
            dragon.set_action("talk")
            user_input = result
            if user_input == "hello":
                bubble = SpeechBubble(text="wagwan")
            if user_input == "1":
                bubble = SpeechBubble(text="heeeeeeeeeeeeeeeee")
            if user_input == "2":
                bubble = SpeechBubble(text="wagwaaaaaaaaaaaaaaaaaaaaaaaaaaaaan")
            elif user_input == "ok":
                bubble = SpeechBubble(text="Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh Bleh ")
            else:
                x = emotion_react.dragon_output(user_input, dragon.get_health())
                dragon.set_mood(x[1])
                bubble = SpeechBubble(text=x[0])
                
            
    if pygame.time.get_ticks() - last_anim_update > 333:
        last_anim_update = pygame.time.get_ticks()
        sprite_value = (sprite_value + 1) % 6
        dragon.change_health(-10)
    
    if dragon.get_action() == "breathe_fire":
        if sprite_value == 0:
            cheppie = "neutral1"
        else:
            cheppie = "fire" + str(sprite_value + 1)
            if sprite_value == 5:
                dragon.set_action("idle")
    else:
        sprite_value = sprite_value % 2
        cheppie = dragon.get_mood() + str(sprite_value + 1)
        if dragon.get_action() == "talk" and sprite_value==1:
            cheppie = "talk" + cheppie


    window.update(cheppie, dragon.get_health())
    textbox.draw(window._Window__screen)
    bubble.draw(window._Window__screen)
    pygame.display.update()