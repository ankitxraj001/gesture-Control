import cv2
import mediapipe as mp
import time

from gestures.hand_gestures import get_gesture
from actions.scroll import scroll_up, scroll_down, click

# ── Settings (no config file needed!) ──────────────────
SCROLL_SPEED      = 3
FAST_SCROLL_SPEED = 9
COOLDOWN          = 0.1
CAMERA_INDEX      = 0

# ── Setup MediaPipe ─────────────────────────────────────
mp_hands = mp.solutions.hands
mp_draw  = mp.solutions.drawing_utils

# ── Main Function ───────────────────────────────────────
def main():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    last_action_time = 0

    print("=" * 40)
    print("   Gesture Control is ACTIVE!")
    print("=" * 40)
    print("1 finger UP    = Scroll Up")
    print("1 finger DOWN  = Scroll Down")
    print("2 fingers      = Fast Scroll Up")
    print("Fist           = Stop")
    print("Pinch          = Click")
    print("Press Q to QUIT")
    print("=" * 40)

    with mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    ) as hands:

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Webcam not found!")
                break

            # Mirror the frame
            frame = cv2.flip(frame, 1)

            # Convert to RGB for MediaPipe
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            gesture = "NONE"

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw hand skeleton
                    mp_draw.draw_landmarks(
                        frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                    )
                    # Get gesture
                    gesture = get_gesture(hand_landmarks)

            # Perform action with cooldown
            now = time.time()
            if now - last_action_time > COOLDOWN:
                if gesture == "SCROLL_UP":
                    scroll_up(SCROLL_SPEED)
                    last_action_time = now
                elif gesture == "SCROLL_DOWN":
                    scroll_down(SCROLL_SPEED)
                    last_action_time = now
                elif gesture == "SCROLL_UP_FAST":
                    scroll_up(FAST_SCROLL_SPEED)
                    last_action_time = now
                elif gesture == "CLICK":
                    click()
                    last_action_time = now

            # Show gesture on screen
            color = (0, 255, 0) if gesture != "NONE" else (200, 200, 200)
            cv2.putText(frame, f"Gesture: {gesture}", (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 2)
            cv2.putText(frame, "Press Q to Quit", (10, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 100, 255), 2)

            cv2.imshow("Gesture Control", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
    print("Gesture Control stopped.")

if __name__ == "__main__":
    main()