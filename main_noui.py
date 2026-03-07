import cv2
import mediapipe as mp
import time

# MediaPipe face detection
mp_face = mp.solutions.face_detection
face_detection = mp_face.FaceDetection(model_selection=0, min_detection_confidence=0.6)

cap = cv2.VideoCapture(0)

greeted = False
last_greet_time = 0
last_seen_time = 0

COOLDOWN = 10
ABSENCE_RESET = 3

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(rgb_frame)

    current_time = time.time()

    if results.detections:
        last_seen_time = current_time

        if not greeted and (current_time - last_greet_time > COOLDOWN):
            print("Face detected - greeting trigger")

            greeted = True
            last_greet_time = current_time

    else:
        absence_time = current_time - last_seen_time

        if absence_time >= ABSENCE_RESET:
            greeted = False

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()