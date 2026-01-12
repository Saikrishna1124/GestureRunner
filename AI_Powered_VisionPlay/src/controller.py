import cv2
from mediapipe.python.solutions import hands as mp_hands
from mediapipe.python.solutions import drawing_utils as mp_draw
import numpy as np
from pynput.keyboard import Controller, Key
import time


def get_action(ix, iy, width, height):
    """Divide screen into 4 zones to decide action with a large deadzone."""
    # Normalized coordinates (-1 to 1)
    nx = (ix - width / 2) / (width / 2)
    ny = (iy - height / 2) / (height / 2)

    # LARGER Deadzone in the middle (35% of the way to the edges)
    deadzone = 0.35
    if abs(nx) < deadzone and abs(ny) < deadzone:
        return None

    if abs(nx) > abs(ny):
        return "RIGHT" if nx > 0 else "LEFT"
    else:
        return "DOWN" if ny > 0 else "UP"


def main():
    keyboard = Controller()

    print("--- FINGER CONTROLLER STARTING ---")
    
    # Robust Camera Initialization
    cap = None
    for index in [0, 1]:
        print(f"Trying to open Camera {index}...")
        # Try DSHOW first (standard for Windows)
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        if cap is not None and cap.isOpened():
            break
        # Try MSMF (modern Windows)
        cap = cv2.VideoCapture(index, cv2.CAP_MSMF)
        if cap is not None and cap.isOpened():
            break
        # Try Auto
        cap = cv2.VideoCapture(index)
        if cap is not None and cap.isOpened():
            break
    
    if cap is None or not cap.isOpened():
        print("CRITICAL ERROR: Could not turn on the camera.")
        print("Please ensure your webcam is plugged in and not used by another app.")
        return

    print("Webcam is now ON. Loading Hand Detection AI...")
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    )
    
    last_action_time = 0
    action_cooldown = 0.3
    last_action = None

    while True:
        ret, frame = cap.read()
        if not ret: break

        frame = cv2.flip(frame, 1)
        frame_h, frame_w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Draw Zone Lines (X shape)
        cv2.line(frame, (0, 0), (frame_w, frame_h), (50, 50, 50), 1)
        cv2.line(frame, (frame_w, 0), (0, frame_h), (50, 50, 50), 1)
        
        # Draw the Deadzone Rectangle (Visual Guide)
        deadzone = 0.35
        # Convert deadzone % to pixel coordinates
        x1 = int(frame_w / 2 * (1 - deadzone))
        y1 = int(frame_h / 2 * (1 - deadzone))
        x2 = int(frame_w / 2 * (1 + deadzone))
        y2 = int(frame_h / 2 * (1 + deadzone))
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 1)
        cv2.putText(frame, "DEADZONE", (x1 + 5, y1 + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        results = hands.process(rgb_frame)
        current_action = None

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Track Index Finger Tip
                tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                ix, iy = int(tip.x * frame_w), int(tip.y * frame_h)
                
                # Draw hand
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                cv2.circle(frame, (ix, iy), 12, (255, 0, 255), -1)

                current_action = get_action(ix, iy, frame_w, frame_h)
        else:
            cv2.putText(frame, "HAND NOT DETECTED", (frame_w//4, frame_h//2), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        # Action Handling
        now = time.time()
        if current_action and current_action != last_action and (now - last_action_time > action_cooldown):
            print(f">>> TRIGGER: {current_action}")
            if current_action == "LEFT": keyboard.press(Key.left); keyboard.release(Key.left)
            elif current_action == "RIGHT": keyboard.press(Key.right); keyboard.release(Key.right)
            elif current_action == "UP": keyboard.press(Key.up); keyboard.release(Key.up)
            elif current_action == "DOWN": keyboard.press(Key.down); keyboard.release(Key.down)
            
            last_action_time = now
            last_action = current_action

        # HUD
        color = (0, 255, 0) if current_action else (200, 200, 200)
        cv2.putText(frame, f"ACTION: {current_action or 'NONE'}", (10, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
        cv2.putText(frame, "Press 'Q' to Exit", (10, frame_h - 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        cv2.imshow("Subway Surfers Finger Controller", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

