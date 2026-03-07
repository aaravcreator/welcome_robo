import cv2
import mediapipe as mp
import pyttsx3
import time

# MediaPipe face detection
mp_face = mp.solutions.face_detection
mp_draw = mp.solutions.drawing_utils
face_detection = mp_face.FaceDetection(model_selection=0, min_detection_confidence=0.6)

# Voice engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

cap = cv2.VideoCapture(0)

greeted = False
last_greet_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(rgb_frame)

    if results.detections:
        for detection in results.detections:
            mp_draw.draw_detection(frame, detection)
        print("Face detected!")
        print(last_greet_time)
        if not greeted or time.time() - last_greet_time > 5:
            engine.say("Namaste! Welcome to our school.")
            engine.runAndWait()
            greeted = True

            last_greet_time = time.time()
    else:
        greeted = False

    cv2.imshow("Welcome Robot Camera", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
