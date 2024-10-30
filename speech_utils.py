import pyttsx3
import speech_recognition as sr
import winsound

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def play_buzzer():
    winsound.Beep(1000, 500)  
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        play_buzzer()
        print("Titan: Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            speak("Sorry, my speech service is down.")
            return None
