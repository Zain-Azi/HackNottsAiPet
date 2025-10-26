import os

import pygame
import serial
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play

import emotion_react
from dragon import Dragon
from feedbutton import FeedButton
from speechbubble import SpeechBubble
from textbox import TextBox
from window import Window

# Arduino serial setup
try:
    arduino = serial.Serial('COM5', 9600, timeout=1)#
except:
    print("tried")
    arduino = None

load_dotenv()
elevenlabs = ElevenLabs(

    api_key=os.getenv("ELEVENLABS_API_KEY"),

)
window_w = 1280
window_h = 720

textbox_w = 1100
textbox_h = 60
textbox_x = (window_w - textbox_w) // 2
textbox_y = window_h - textbox_h - 20
pygame_icon = pygame.image.load('assets\idle1.PNG')
pygame.display.set_icon(pygame_icon)
clock = pygame.time.Clock()
FPS = 30

dragon = Dragon("Cheppie")

window = Window("Cheppie the Dragon", window_w, window_h)
textbox = TextBox(textbox_x, textbox_y, textbox_w, textbox_h)
bubble = SpeechBubble(text="Hello, I am "+ dragon.get_name()+"!")
feedbutton = FeedButton(15, window_h - 150, 100, 50)

exit = False

sprite_value = 0
ta = 0

last_anim_update = pygame.time.get_ticks()

while not exit:
    clock.tick(FPS)
    
    #Arduino button
    try:
        if arduino.in_waiting > 0:
            line = arduino.readline().decode().strip()
            if line == "pressed":
                dragon.set_action("breathe_fire")
                dragon.change_health(-50)
    except:
        pass
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit = True
            if event.key == pygame.K_LCTRL:
                dragon.set_action("breathe_fire")
                dragon.change_health(-50)
            
        if feedbutton.handle_event(event):
            dragon.change_health(100)

        result = textbox.handle_event(event)
        if os.path.exists("temp_audio.mp3"):
            os.remove("temp_audio.mp3")
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

            try:
                audio = elevenlabs.text_to_speech.convert(
                    text=bubble.get_text(),
                    voice_id="EDO68oHvNm0rxTewQZSK",
                    model_id="eleven_multilingual_v2",
                    output_format="mp3_44100_128",
                )

                audio_bytes = b"".join(audio)

                
                with open(f"temp_audio{ta}.mp3", "wb") as f:
                    f.write(audio_bytes)
                    
                if not pygame.mixer.get_init():
                    pygame.mixer.music.stop()
                    pygame.mixer.quit()
                    pygame.mixer.init()
                pygame.mixer.music.load(f"temp_audio{ta}.mp3")
                pygame.mixer.music.play()
                ta += 1
            except:
                pass


            with open("chatlog.txt", "a") as f:
                f.write("YOU: " + user_input + "\nCheppie: " + bubble.get_text() + "\n")

                
            
    if pygame.time.get_ticks() - last_anim_update > 333:
        last_anim_update = pygame.time.get_ticks()
        sprite_value = (sprite_value + 1) % 6
        dragon.change_health(-2)
    
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
    feedbutton.draw(window._Window__screen)
    pygame.display.update()

for f in os.listdir():
    if f.startswith("temp_audio"):
        try:
            os.remove(f)
        except PermissionError:
            print(f"Could not delete {f} (still in use).")
pygame.quit()
