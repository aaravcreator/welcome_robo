# Welcome Robot

A face detection and voice greeting system that welcomes visitors at entry points using computer vision and text-to-speech technology.

## Features

- **Real-time Face Detection**: Uses MediaPipe for efficient face detection
- **Voice Greeting**: Automatically greets detected visitors with audio message
- **Smart Cooldown System**: Prevents repetitive greetings with configurable cooldown timers
- **Visual Feedback**: Live camera feed with status display showing detection state and timers
- **Cross-Platform**: Works on macOS, Windows, and Linux with webcam support

## How It Works

The application monitors a webcam feed for face detections:

1. **Detection**: When a face is detected, it's marked with a bounding box
2. **Greeting**: If enough time has passed since the last greeting (cooldown period), the system greets the visitor with an audio message: "Namaste! Welcome to our school."
3. **Cooldown**: After greeting, a 10-second cooldown begins. During this time, the same person won't be greeted again
4. **Reset**: If the face disappears for 3+ seconds, the state resets and the person can be greeted again

## Configuration

Key parameters in `main.py`:

- `COOLDOWN = 10`: Seconds to wait before greeting the same person again
- `ABSENCE_RESET = 3`: Seconds a face must be absent before resetting the greeting state
- `min_detection_confidence=0.6`: Face detection confidence threshold (0.0-1.0)

## Requirements

- Python 3.8+
- Webcam access

## Installation

1. Create and activate a virtual environment:

```bash
python3 -m venv myenv
source myenv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the application:

```bash
python main.py
```

**Controls:**

- Press `ESC` to exit the application

## Display Indicators

The application shows a status panel with:

- **Status**: Current state (NO FACE, READY, GREETING, WAITING)
- **Cooldown Remaining**: Seconds until the next greeting is allowed
- **Absence Reset In**: Seconds until state resets when face is lost

## Dependencies

- `opencv-python`: Computer vision library for camera capture and frame processing
- `mediapipe`: Face detection model
- `pyttsx3`: Text-to-speech engine for voice output
- `numpy`: Numerical computing
- `matplotlib`: (included with dependencies)
