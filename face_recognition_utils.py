import dlib
import numpy as np
import cv2
import pickle
import os
import time

# Load the shape predictor model
shape_predictor_path = r"C:\Users\rocro\OneDrive\Desktop\Vscode\Titan\Modules\shape_predictor_68_face_landmarks.dat"
shape_predictor = dlib.shape_predictor(shape_predictor_path)

# Load the face recognition model
face_rec_model_path = r"C:\Users\rocro\OneDrive\Desktop\Vscode\Titan\Modules\dlib_face_recognition_resnet_model_v1.dat"
face_rec_model = dlib.face_recognition_model_v1(face_rec_model_path)

def encode_face(image, face_location):
    shape = shape_predictor(image, face_location)
    face_encoding = np.array(face_rec_model.compute_face_descriptor(image, shape))
    return face_encoding

def find_closest_match(face_encoding, known_encodings, threshold=0.4):
    min_distance = float('inf')
    best_match_name = None
    for name, encoding in known_encodings.items():
        distance = np.linalg.norm(encoding - face_encoding)
        if distance < min_distance:
            min_distance = distance
            best_match_name = name
    if min_distance < threshold:
        return best_match_name
    return None

def recognize_face(known_encodings):
    video_capture = cv2.VideoCapture(0)
    face_found = False
    recognized_name = None
    start_time = time.time()
    while not face_found and (time.time() - start_time) < 15:
        ret, frame = video_capture.read()
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_detector = dlib.get_frontal_face_detector()
        face_locations = face_detector(rgb_frame)

        for face_location in face_locations:
            face_encoding = encode_face(rgb_frame, face_location)
            recognized_name = find_closest_match(face_encoding, known_encodings)

            if recognized_name:
                face_found = True
                break

        cv2.imshow("Video", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return face_found, recognized_name

def save_face_encoding(name, face_encoding):
    encodings_file = 'encodings.pkl'
    if os.path.exists(encodings_file):
        with open(encodings_file, 'rb') as file:
            known_encodings = pickle.load(file)
    else:
        known_encodings = {}

    known_encodings[name] = face_encoding
    with open(encodings_file, 'wb') as file:
        pickle.dump(known_encodings, file)

def load_known_encodings():
    encodings_file = 'encodings.pkl'
    if os.path.exists(encodings_file):
        with open(encodings_file, 'rb') as file:
            known_encodings = pickle.load(file)
        return known_encodings
    else:
        return {}
