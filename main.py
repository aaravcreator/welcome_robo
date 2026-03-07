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
last_seen_time = 0

COOLDOWN = 10          # seconds before greeting again
ABSENCE_RESET = 3      # seconds face must be gone before reset

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(rgb_frame)

    current_time = time.time()
    status_text = "NO FACE"

    cooldown_remaining = max(0, int(COOLDOWN - (current_time - last_greet_time)))
    absence_remaining = 0

    if results.detections:
        last_seen_time = current_time

        for detection in results.detections:
            mp_draw.draw_detection(frame, detection)

        if not greeted and (current_time - last_greet_time > COOLDOWN):
            status_text = "GREETING..."
            cv2.putText(frame, status_text, (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("Welcome Robot Camera", frame)
            cv2.waitKey(1)

            engine.say("Namaste! Welcome to our school.")
            engine.runAndWait()

            greeted = True
            last_greet_time = current_time
        else:
            status_text = f"WAITING ({cooldown_remaining}s)"

    else:
        absence_time = current_time - last_seen_time

        if absence_time < ABSENCE_RESET:
            absence_remaining = round(ABSENCE_RESET - absence_time, 1)
            status_text = f"FACE LOST ({absence_remaining}s reset)"
        else:
            greeted = False
            status_text = "READY"

    # Draw UI Panel Background
    cv2.rectangle(frame, (10, 10), (500, 140), (0, 0, 0), -1)

    cv2.putText(frame, f"Status: {status_text}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    cv2.putText(frame, f"Cooldown Remaining: {cooldown_remaining}s", (20, 75),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    cv2.putText(frame, f"Absence Reset In: {absence_remaining}s", (20, 105),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 255), 2)

    cv2.imshow("Welcome Robot Camera", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()