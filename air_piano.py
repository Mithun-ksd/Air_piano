import cv2
import mediapipe as mp
import pygame
import math
import array
import sys

# -------------------- INITIALIZATION --------------------

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

W, H = 900, 360

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Air Piano")

font = pygame.font.Font(None, 30)

# -------------------- WEBCAM --------------------

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Could not open webcam.")
    pygame.quit()
    sys.exit()

# -------------------- GENERATE PIANO SOUNDS --------------------

def make_tone(freq, duration=0.18, volume=0.25, sample_rate=44100):
    """Generate a piano note using a sine wave."""
    n = int(sample_rate * duration)

    data = array.array(
        "h",
        (
            int(
                32767
                * volume
                * math.sin(2 * math.pi * freq * i / sample_rate)
            )
            for i in range(n)
        )
    )

    return pygame.mixer.Sound(buffer=data.tobytes())


frequencies = [262, 294, 330, 349, 392, 440, 494]
note_names = ["C", "D", "E", "F", "G", "A", "B"]

try:
    sounds = [make_tone(freq) for freq in frequencies]
except Exception as error:
    print("Audio initialization error:", error)
    sounds = [None] * 7

# -------------------- MEDIAPIPE HAND TRACKING --------------------

hands_api = mp.solutions.hands

last_key = -1
running = True

print("Air Piano started!")
print("Point with your index finger to play notes.")
print("Press ESC in the piano window or Q in the camera window to exit.")

try:
    # Initialize the detector only once.
    with hands_api.Hands(
        static_image_mode=False,
        max_num_hands=1,
        model_complexity=0,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.5
    ) as hands:

        # -------------------- MAIN LOOP --------------------

        while running:

            # Handle keyboard and window events.
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                elif (
                    event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE
                ):
                    running = False

            if not running:
                break

            # Read webcam frame.
            ok, frame = cap.read()

            if not ok:
                print("ERROR: Could not read webcam frame.")
                break

            # Mirror the camera image.
            frame = cv2.flip(frame, 1)

            # Convert the frame to RGB for MediaPipe.
            rgb_frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            # Improve processing performance.
            rgb_frame.flags.writeable = False
            result = hands.process(rgb_frame)
            rgb_frame.flags.writeable = True

            # -------------------- DRAW PIANO --------------------

            screen.fill((25, 28, 48))

            key_width = W // 7
            key_now = -1

            # Find the index fingertip.
            if result.multi_hand_landmarks:
                landmarks = result.multi_hand_landmarks[0]

                tip = landmarks.landmark[8]

                # Convert normalized coordinates to screen coordinates.
                px = int(tip.x * W)
                py = int(tip.y * H)

            else:
                px, py = -1, -1

            # Draw seven piano keys.
            for i in range(7):

                rect = pygame.Rect(
                    i * key_width + 2,
                    80,
                    key_width - 4,
                    220
                )

                active = rect.collidepoint(px, py)

                if active:
                    key_now = i

                key_color = (
                    (255, 205, 75)
                    if active
                    else (238, 241, 250)
                )

                pygame.draw.rect(
                    screen,
                    key_color,
                    rect,
                    border_radius=6
                )

                # Draw note label.
                label = font.render(
                    note_names[i],
                    True,
                    (25, 25, 35)
                )

                screen.blit(
                    label,
                    (
                        rect.centerx - label.get_width() // 2,
                        rect.bottom - 35
                    )
                )

            # -------------------- PLAY NOTES --------------------

            # Play a note only when entering a different key.
            if (
                key_now >= 0
                and key_now != last_key
                and sounds[key_now] is not None
            ):
                sounds[key_now].play()

            last_key = key_now

            # -------------------- DISPLAY INSTRUCTIONS --------------------

            title = font.render(
                "AIR PIANO - Point with index finger | ESC to quit",
                True,
                (255, 255, 255)
            )

            screen.blit(title, (20, 25))

            pygame.display.flip()

            # Display the camera window.
            cv2.imshow("Air Piano Camera - Press Q to quit", frame)

            # Press Q to exit.
            if cv2.waitKey(1) & 0xFF == ord("q"):
                running = False

finally:
    # -------------------- CLEANUP --------------------

    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()

    print("Air Piano closed successfully.")
