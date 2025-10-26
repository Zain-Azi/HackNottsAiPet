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
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
import os

from vosk import Model, KaldiRecognizer
import pyaudio, json, threading

class VoskRecorder:
   def __init__(self, model_path="vosk-model-small-en-us-0.15", sample_rate=16000):
       self.model = Model(model_path)
       self.sample_rate = sample_rate
       self.p = pyaudio.PyAudio()
       self.stream = None
       self.recognizer = None
       self.thread = None
       self.stop_event = threading.Event()
       self._text_lock = threading.Lock()
       self._text = []


   def _loop(self):
       while not self.stop_event.is_set():
           data = self.stream.read(4096, exception_on_overflow=False)
           if self.recognizer.AcceptWaveform(data):
               result = json.loads(self.recognizer.Result())
               t = result.get("text", "").strip()
               if t:
                   with self._text_lock:
                       self._text.append(t)
       final = json.loads(self.recognizer.FinalResult())
       t = final.get("text", "").strip()
       if t:
           with self._text_lock:
               self._text.append(t)


   def start(self):
       if self.thread and self.thread.is_alive():
           return
       self.stop_event.clear()
       self.recognizer = KaldiRecognizer(self.model, self.sample_rate)
       self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=self.sample_rate,
                                 input=True, frames_per_buffer=8192)
       self.stream.start_stream()
       with self._text_lock:
           self._text = []
       self.thread = threading.Thread(target=self._loop, daemon=True)
       self.thread.start()
       print("🎙️ recording started")


   def stop(self) -> str:
       if not self.thread:
           return ""
       self.stop_event.set()
       self.thread.join()
       self.stream.stop_stream()
       self.stream.close()
       self.stream = None
       self.thread = None
       text = ""
       with self._text_lock:
           text = " ".join(self._text).strip()
           self._text = []
       print("🛑 recording stopped")
       return text

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
        print("tried")
    
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
                bubble = SpeechBubble(text="Bleh")
            else:
                x = emotion_react.dragon_output(user_input, dragon.get_health())
                dragon.set_mood(x[1])
                bubble = SpeechBubble(text=x[0])
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


            with open("chatlog.txt", "a") as f:
               f.write("YOU: " + str(user_input) + "\nCheppie: " + bubble.get_text() + "\n")


                
            
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
