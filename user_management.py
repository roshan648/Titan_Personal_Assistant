import pickle
import os
from speech_utils import speak 
def list_users():
    encodings_file = 'encodings.pkl'
    if os.path.exists(encodings_file):
        with open(encodings_file, 'rb') as file:
            known_encodings = pickle.load(file)
        users = ", ".join(known_encodings.keys())
        speak(f"Currently recognized users are: {users}")
    else:
        speak("No users are currently recognized.")

def delete_user_face(name, passcode):
    if passcode == "hyper":
        encodings_file = 'encodings.pkl'
        if os.path.exists(encodings_file):
            with open(encodings_file, 'rb') as file:
                known_encodings = pickle.load(file)
            if name in known_encodings:
                del known_encodings[name]
                with open(encodings_file, 'wb') as file:
                    pickle.dump(known_encodings, file)
                speak(f"Face encoding for {name} has been deleted.")
            else:
                speak("No such user found.")
        else:
            speak("No user encodings found.")
    else:
        speak("Incorrect passcode.")
