import cv2
import mediapipe as mp
import pyttsx3
import time
import requests
import serial

# ==============================
# COMMUNICATION MODE
# ==============================
USE_SERIAL = False      # True = Serial , False = WiFi
reset_sent = False
# WIFI SETTINGS
esp32_ip = "192.168.4.1"

# SERIAL SETTINGS
SERIAL_PORT = "/dev/cu.usbserial-1130"
# SERIAL_PORT = "/dev/ttyUSB0" # for linux   # change if needed
BAUD_RATE = 115200

# ==============================

# Setup serial if enabled
ser = None
if USE_SERIAL:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
    print("Serial connected to ESP32")

# MediaPipe face detection
mp_face = mp.solutions.face_detection
face_detection = mp_face.FaceDetection(model_selection=0, min_detection_confidence=0.6)

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

    print(f"[CMD] {command}")

    if USE_SERIAL:
        if command == "greet_raise":
            command = "g"
        elif command == "greet_lower":
            command = "l"
        try:
            ser.write((command).encode())
            print("[SERIAL] Command sent")
        except Exception as e:
            print("[SERIAL ERROR]", e)

    else:
        try:
            response = requests.get(f"http://{esp32_ip}/{command}", timeout=2)
            if response.status_code == 200:
                print("[WIFI] Command sent successfully")
            else:
                print("[WIFI] Failed:", response.status_code)
        except Exception as e:
            print("[WIFI ERROR]", e)


while True:

    ret, frame = cap.read()
    if not ret:
        print("Camera read failed")
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(rgb_frame)

    current_time = time.time()

    cooldown_remaining = max(0, int(COOLDOWN - (current_time - last_greet_time)))
    absence_remaining = 0
    status_text = "NO FACE"

    if results.detections:
        reset_sent = False

        last_seen_time = current_time
        print("[INFO] Face detected")

        if not greeted and (current_time - last_greet_time > COOLDOWN):

            status_text = "GREETING..."

            print("================================")
            print("[STATUS]", status_text)
            print("================================")

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

        elif not reset_sent:

            status_text = "FACE LOST (Resetting...)"

            print("********************************")
            print("######## FACE LOST ########")
            print("********************************")

            send_command("greet_lower")

            reset_sent = True
            greeted = False

        else:
            status_text = "READY"

    print(
        f"[STATUS] {status_text} | Cooldown: {cooldown_remaining}s | Absence reset: {absence_remaining}s"
    )

    time.sleep(0.1)

cap.release()

if ser:
    ser.close()