import cv2
import face_recognition
import numpy as np
import os
import serial
import time

# ====== Optional ESP32 Serial ======
# esp = serial.Serial('/dev/ttyUSB0', 115200)

# ====== Load Known Faces ======
known_encodings = []
known_names = []

for file in os.listdir("known_faces"):
    image = face_recognition.load_image_file(f"known_faces/{file}")
    encoding = face_recognition.face_encodings(image)[0]
    known_encodings.append(encoding)
    known_names.append(os.path.splitext(file)[0])

# ====== Camera ======
video = cv2.VideoCapture(0)

process_frame = True
last_greet_time = 0

while True:
    ret, frame = video.read()
    small_frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
    rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    if process_frame:
        face_locations = face_recognition.face_locations(rgb_small)
        face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

        face_names = []

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            name = "Guest"

            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_names[best_match_index]

            face_names.append(name)

            # Greeting cooldown
            if time.time() - last_greet_time > 5:
                if name != "Guest":
                    os.system(f'espeak "Namaste {name}! Welcome back."')
                else:
                    os.system('espeak "Namaste! Welcome to our school."')

                # esp.write(b'NAMASTE\n')
                last_greet_time = time.time()

    process_frame = not process_frame

    # Draw results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 2
        right *= 2
        bottom *= 2
        left *= 2

        cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)
        cv2.putText(frame, name, (left, top-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

    cv2.imshow("Smart Welcome Robot", frame)

    if cv2.waitKey(1) == 27:
        break

video.release()
cv2.destroyAllWindows()
