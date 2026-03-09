import cv2
import mediapipe as mp
import pyttsx3
import time
import requests

# MediaPipe face detection
mp_face = mp.solutions.face_detection
face_detection = mp_face.FaceDetection(model_selection=0, min_detection_confidence=0.6)

esp32_ip = "192.168.4.1"
# Voice engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

cap = cv2.VideoCapture(0)

greeted = False
last_greet_time = 0
last_seen_time = 0

COOLDOWN = 10
ABSENCE_RESET = 3

def send_command(command):
    print(f"Sending command: {command} to ESP32 at {esp32_ip}")
    try:
        response = requests.get(f"http://{esp32_ip}/{command}", timeout=2)
        if response.status_code == 200:
            print("Command sent successfully")
        else:
            print(f"Failed to send command, status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error sending command: {e}")


while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(rgb_frame)

    current_time = time.time()

    cooldown_remaining = max(0, int(COOLDOWN - (current_time - last_greet_time)))
    absence_remaining = 0
    status_text = "NO FACE"

    if results.detections:
        last_seen_time = current_time

        if not greeted and (current_time - last_greet_time > COOLDOWN):
            status_text = "GREETING..."
            print("**********************************")
            print("################Face detected #############")
            print("################Face detected #############")
            print("####################################")
            print("**********************************")
            print("Status:", status_text)

            # engine.say("Namaste! Welcome to our school.")
            # engine.runAndWait()
            send_command("greet_raise")

            greeted = True
            last_greet_time = current_time

        else:
            status_text = f"WAITING ({cooldown_remaining}s)"

    else:
        absence_time = current_time - last_seen_time

        if absence_time < ABSENCE_RESET:
            absence_remaining = round(ABSENCE_RESET - absence_time, 1)
            status_text = f"FACE LOST ({absence_remaining}s reset)"
        elif absence_time - ABSENCE_RESET <=1:
                status_text = f"FACE LOST (Resetting...)"
                print("**********************************")
                print("################Face lost #############")
                print("################Face lost #############")
                print("####################################")
                print("**********************************")
                print("Status:", status_text)
                send_command("greet_lower")  
        else:
            greeted = False
            status_text = "READY"

    print(
        f"Status: {status_text} | "
        f"Cooldown Remaining: {cooldown_remaining}s | "
        f"Absence Reset In: {absence_remaining}s"
    )

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()