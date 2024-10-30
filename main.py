import smtplib, ssl
import dlib
import numpy as np
import cv2
import time
import re
from PIL import Image
from speech_utils import speak, listen
from face_recognition_utils import recognize_face, save_face_encoding, load_known_encodings, encode_face, find_closest_match
from app_utils import open_application, close_application, open_youtube, open_browser, open_spotify
from weather_utils import get_weather, get_location
from music_utils import play_music
from user_management import list_users, delete_user_face
from system_utils import set_system_volume, mute_system_volume, unmute_system_volume, increase_volume, decrease_volume, connect_to_wifi, shutdown_system, reboot_system, set_brightness, get_current_brightness, show_battery_percentage, get_wifi_credentials
from mqtt_utils import ring_buzzer
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
import io

def send_email_with_attachments(subject, body, sender_email, password, receiver_email, attachments):
    # Create the email
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Add body
    msg.attach(MIMEText(body, 'plain'))

    # Attach files
    for file_path in attachments:
        with open(file_path, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {file_path.split("/")[-1]}',
            )
            msg.attach(part)

    # Send the email
    try:
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully.")
        speak("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

def capture_face_and_video(image_filename, video_filename):
    video_capture = cv2.VideoCapture(0)
    face_detector = dlib.get_frontal_face_detector()
    start_time = time.time()
    face_detected = False

    # Capture the face image
    while (time.time() - start_time) < 15:
        ret, frame = video_capture.read()
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_detector(rgb_frame)

        if face_locations:
            # Save the face image
            cv2.imwrite(image_filename, frame)
            face_detected = True
            break

    # Record a 5-second video clip
    video_writer = cv2.VideoWriter(video_filename, cv2.VideoWriter_fourcc(*'XVID'), 20.0, (640, 480))
    start_time = time.time()
    while (time.time() - start_time) < 5:
        ret, frame = video_capture.read()
        if ret:
            video_writer.write(frame)
    
    video_capture.release()
    video_writer.release()
    cv2.destroyAllWindows()

    return face_detected

def register_new_user(known_encodings):
    speak("No known faces available. Please show your face to register as a new user.")
    video_capture = cv2.VideoCapture(0)
    start_time = time.time()
    face_detected = False

    while (time.time() - start_time) < 15:
        ret, frame = video_capture.read()
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_detector = dlib.get_frontal_face_detector()
        face_locations = face_detector(rgb_frame)

        for face_location in face_locations:
            new_face_encoding = encode_face(rgb_frame, face_location)
            speak("Please tell me your name for this new face.")
            new_name = listen()
            if new_name:
                save_face_encoding(new_name, new_face_encoding)
                known_encodings[new_name] = new_face_encoding  # Update known encodings
                speak(f"New face for {new_name} has been added.")
                face_detected = True
                break

        cv2.imshow("Video", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

    if not face_detected:
        speak("No face detected within the time limit.")

def main():
    known_encodings = load_known_encodings()
    owner_email = "roshanrockga@gmail.com"  # Replace with actual owner email
    owner_password = "opci tsop xjqb lpbp"  # Replace with actual owner email password

    if not known_encodings:
        register_new_user(known_encodings)
        if not known_encodings:
            speak("No faces were registered. Exiting.")
            return

    speak("Please show your face for identification.")
    face_found, recognized_name = recognize_face(known_encodings)

    if face_found:
        speak(f"Hi {recognized_name}! How can I help you today?")
        while True:
            command = listen()
            if command:
                print(f"{recognized_name}: {command}")
                speak(f"You said: {command}")

                command = command.lower()

                if "where is my smoke detector" in command:
                    ring_buzzer()
                    speak("The buzzer is ringing.")
                elif "who are you" in command:
                    speak("I am Titan, your Personal Assistant.")
                elif "hello" in command:
                    speak(f"Hello, {recognized_name}! How are you?")
                elif "time" in command:
                    from datetime import datetime
                    current_time = datetime.now().strftime("%I:%M %p")
                    speak(f"The time is {current_time}")
                elif "stop" in command:
                    speak("Goodbye!")
                    break
                elif "volume" in command:
                    if "increase" in command:
                        match = re.search(r"increase volume by (\d+)", command)
                        if match:
                            amount = int(match.group(1))
                            increase_volume(amount)
                            speak(f"Increased volume by {amount}.")
                        else:
                            speak("Please specify a valid volume level.")
                    elif "decrease" in command:
                        match = re.search(r"decrease volume by (\d+)", command)
                        if match:
                            amount = int(match.group(1))
                            decrease_volume(amount)
                            speak(f"Decreased volume by {amount}.")
                        else:
                            speak("Please specify a valid volume level.")
                    elif "set" in command:
                        try:
                            level = int(re.search(r"set volume to (\d+)", command).group(1))
                            if 0 <= level <= 100:
                                set_system_volume(level)
                                speak(f"System volume set to {level}.")
                            else:
                                speak("Please specify a valid volume level between 0 and 100.")
                        except (ValueError, AttributeError):
                            speak("Please specify a valid volume level.")
                    elif "mute" in command:
                        if "unmute" in command:
                            unmute_system_volume()
                            speak("System volume unmuted.")
                        else:
                            mute_system_volume()
                            speak("System volume muted.")
                    else:
                        speak("Volume command not recognized.")
                elif "search" in command:
                    search_query = command.split("search", 1)[-1].strip()
                    if search_query:
                        open_browser(search_query)
                        speak(f"Searching for {search_query}.")
                elif "brightness" in command:
                    if "set" in command:
                        try:
                            level = int(re.search(r"set brightness to (\d+)", command).group(1))
                            if 0 <= level <= 100:
                                set_brightness(level)
                                speak(f"Screen brightness set to {level}.")
                            else:
                                speak("Please specify a valid brightness level between 0 and 100.")
                        except (ValueError, AttributeError):
                            speak("Please specify a valid brightness level.")
                    elif "get" in command:
                        brightness = get_current_brightness()
                        speak(f"Current screen brightness is {brightness}%.")
                    else:
                        speak("Brightness command not recognized.")
                elif "battery" in command:
                    if "percentage" in command:
                        battery_message = show_battery_percentage()
                        speak(battery_message)
                    else:
                        speak("Battery command not recognized.")
                elif "internet" in command:
                    ssid, password = get_wifi_credentials()
                    if ssid and password:
                        connect_to_wifi(ssid, password)
                        speak(f"Connecting to Wi-Fi network {ssid}.")
                    else:
                        speak("No Wi-Fi credentials provided.")
                elif "shutdown" in command:
                    speak("Shutting down the system.")
                    shutdown_system()
                elif "reboot" in command:
                    speak("Rebooting the system.")
                    reboot_system()
                elif "add new face" in command:
                    speak("Please show your face for capturing.")
                    video_capture = cv2.VideoCapture(0)
                    start_time = time.time()
                    face_detected = False

                    while (time.time() - start_time) < 15:
                        ret, frame = video_capture.read()
                        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        face_detector = dlib.get_frontal_face_detector()
                        face_locations = face_detector(rgb_frame)

                        for face_location in face_locations:
                            new_face_encoding = encode_face(rgb_frame, face_location)
                            existing_name = find_closest_match(new_face_encoding, known_encodings)

                            if existing_name:
                                speak(f"You are already recognized as {existing_name}.")
                                face_detected = True
                                break
                            else:
                                speak("Please tell me your name for this new face.")
                                new_name = listen()
                                if new_name:
                                    save_face_encoding(new_name, new_face_encoding)
                                    known_encodings[new_name] = new_face_encoding  # Update known encodings
                                    speak(f"New face for {new_name} has been added.")
                                    face_detected = True
                                    break

                        cv2.imshow("Video", frame)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break

                    video_capture.release()
                    cv2.destroyAllWindows()

                    if not face_detected:
                        speak("No face detected within the time limit.")
                elif "delete face" in command:
                    speak("Please provide the passcode to delete a user's face.")
                    passcode = listen()
                    if passcode:
                        if passcode == "hyper":
                            speak("Please tell me the name of the user whose face you want to delete.")
                            name_to_delete = listen()
                            if name_to_delete:
                                delete_user_face(name_to_delete)
                                speak(f"Face data for {name_to_delete} has been deleted.")
                        else:
                            speak("Incorrect passcode.")
                elif "play music" in command:
                    play_music()
                elif "weather" in command:
                    location = get_location()
                    if location:
                        weather = get_weather(location)
                        speak(f"The current weather in {location} is {weather}.")
                    else:
                        speak("Location not found.")
                elif "open youtube" in command:
                    speak("What do you want to search for on YouTube?")
                    search_query = listen()
                    if search_query:
                        open_youtube(search_query)
                        speak(f"Opening YouTube with search query: {search_query}.")
                    else:
                        speak("No search query provided.")
                elif "open spotify" in command:
                    speak("What do you want to search for on Spotify?")
                    search_query = listen()
                    if search_query:
                        open_spotify(search_query)
                        speak(f"Opening Spotify with search query: {search_query}.")
                    else:
                        speak("No search query provided.")
                elif "open application" in command:
                    app_name = re.search(r"open (.+)", command).group(1)
                    open_application(app_name)
                elif "close application" in command:
                    app_name = re.search(r"close (.+)", command).group(1)
                    close_application(app_name)
                elif "list users" in command:
                    users = list_users()
                    if users:
                        speak(f"Registered users: {', '.join(users)}.")
                    else:
                        speak("No users found.")
                else:
                    speak("Command not recognized.")
    else:
        speak("Face not recognized. Capturing face and video.")
        image_file = "unknown_face.jpg"
        video_file = "unknown_face.mp4"

        face_detected = capture_face_and_video(image_file, video_file)

        if face_detected:
            subject = "Unknown Face Detected"
            body = "An unknown face was detected. Please find the attached images and video."
            attachments = [image_file, video_file]
            speak("Face Detected")
            send_email_with_attachments(subject, body, owner_email, owner_password, owner_email, attachments)
        else:
            subject = "Unknown Face Detected"
            body = "An unknown face was detected. Please find the attached images and video."
            attachments = [video_file]
            speak("No face detected during capture.")
            send_email_with_attachments(subject, body, owner_email, owner_password, owner_email, attachments)


if __name__ == "__main__":
    main()
