# Air Piano

Air Piano is a touch-free virtual piano controlled by your index fingertip. It uses a webcam and MediaPipe Hands to track the hand, then maps the fingertip position to one of seven on-screen keys: **C, D, E, F, G, A, B**. When the fingertip moves onto a different key, the program plays the corresponding synthesized tone.

## Concept

The project demonstrates real-time hand tracking and gesture-based interaction. Instead of touching a physical keyboard, the user points at keys displayed on the screen.

## Model Definition

This project uses the **MediaPipe Hands** pretrained hand-tracking solution. It detects a hand and returns normalized landmark coordinates. The program reads landmark `8`, the index fingertip, and maps its position to the piano display.

No custom model is trained. The note sounds are generated mathematically with sine waves rather than loaded from piano recordings.

## How It Works

1. Initialize Pygame and open the webcam using OpenCV.
2. Generate seven short tones from the configured note frequencies.
3. Read each webcam frame and flip it horizontally.
4. Convert the frame from BGR to RGB and process it with MediaPipe Hands.
5. Convert the index-fingertip coordinates to the piano window's coordinate system.
6. Draw seven keys and highlight the key under the fingertip.
7. Play a tone when the fingertip enters a different key.
8. Release the webcam and close the application windows on exit.

## Requirements

- Python 3.9 or newer is a reasonable starting point; use a version supported by your installed MediaPipe release.
- A working webcam and camera permissions.
- A desktop environment that supports Pygame and OpenCV windows.
- Python packages:
  - `opencv-python`
  - `mediapipe`
  - `pygame`

The script also uses Python standard-library modules: `math`, `array`, and `sys`.

## Installation

It is recommended to create a virtual environment.

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install opencv-python mediapipe pygame
```

## Running the Program

If the script is named `air_piano.py`:

```bash
python air_piano.py
```

If you keep the uploaded filename:

```bash
python "air_piano(2).py"
```

## Controls

- Point your index finger at a key in the piano window to play a note.
- Press `Esc` in the piano window or `Q` in the camera window to quit.

## Configuration

- `W, H = 900, 360`: dimensions of the piano window.
- `frequencies`: frequencies used to synthesize the seven notes.
- `make_tone()`: controls tone duration, volume, and sample rate.
- MediaPipe's `min_detection_confidence` and `min_tracking_confidence`: detection/tracking confidence thresholds.

## Troubleshooting

- **Webcam unavailable:** Check camera permissions, close other applications using the camera, or try camera index `1`.
- **No sound:** Check system volume and audio output. Pygame's mixer must initialize correctly.
- **Hand not detected reliably:** Improve lighting and keep the hand visible within the camera frame.
- **Dependency installation fails:** Check Python compatibility with the MediaPipe release available for your operating system.

## Limitations

- Sounds are simple synthesized sine waves, not realistic piano samples.
- Performance depends on lighting, webcam quality, and hand visibility.
- The interface maps fingertip position to keys; it does not detect physical contact.
