import os
import pygame
import time
from urllib.parse import quote
from speech_utils import speak 
import webbrowser

def open_browser(query):
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)

def play_music(song_name):
    music_folder = os.path.expanduser('~/Music')
    song_path = os.path.join(music_folder, song_name)

    if not os.path.exists(song_path):
        speak("Sorry, the song was not found in the default music folder. Searching online.")
        search_online(song_name)
        return

    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()
    speak(f"Playing {song_name}")
    while pygame.mixer.music.get_busy():
        time.sleep(1)

def search_online(query):
    speak("Searching for the song online.")
    open_browser(query)
