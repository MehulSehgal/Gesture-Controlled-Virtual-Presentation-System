import cv2
import mediapipe as mp
import pyautogui
import numpy as np

# Initialize MediaPipe Hands tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280) # Camera Width
cap.set(4, 720)  # Camera Height

# Variables for drawing and swiping logic
annotations = []
prev_x = 0
swipe_threshold = 50  # Minimum horizontal pixel movement to trigger a swipe
cooldown = 0  # Prevents multiple slides from skipping at once

print("\n--- System Ready! ---")
print("Gestures:")
print(" Draw        : Hold Index finger UP (keep middle finger down)")
print(" Next Slide  : Swipe hand RIGHT")
print(" Prev Slide  : Swipe hand LEFT")
print(" Clear Canvas: Press 'c' on your keyboard")
print(" Quit        : Press 'q' on your keyboard\n")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame. Is your webcam being used by another app?")
        break

    # Mirror the image so movement feels natural (like a mirror)
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # Convert BGR to RGB for MediaPipe processing
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    # Reduce the cooldown timer each frame
    if cooldown > 0:
        cooldown -= 1

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw the skeleton on your hand
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Extract specific joint coordinates
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]

            # Convert normalized coordinates (0 to 1) to actual pixel coordinates
            ix, iy = int(index_tip.x * w), int(index_tip.y * h)
            mx, my = int(middle_tip.x * w), int(middle_tip.y * h)
            wx = int(wrist.x * w)

            # GESTURE 1: Drawing
            # Logic: If the index finger is significantly higher than the middle finger
            if iy < my - 40:
                cv2.circle(frame, (ix, iy), 8, (0, 0, 255), cv2.FILLED)
                annotations.append((ix, iy))

            # GESTURE 2: Swiping
            # Logic: Track the wrist's horizontal movement across frames
            if cooldown == 0:
                if prev_x != 0:
                    movement = wx - prev_x
                    if movement > swipe_threshold:
                        pyautogui.press('right')  # Simulates pressing the Right Arrow key
                        print("Swiped Right -> Next Slide")
                        cooldown = 20  # Wait 20 frames before allowing another swipe
                    elif movement < -swipe_threshold:
                        pyautogui.press('left')  # Simulates pressing the Left Arrow key
                        print("Swiped Left <- Previous Slide")
                        cooldown = 20

            prev_x = wx
    else:
        # Reset tracking if the hand leaves the frame
        prev_x = 0

    # Draw all saved annotation points (your drawing trail) on the screen
    for point in annotations:
        cv2.circle(frame, point, 5, (0, 255, 0), cv2.FILLED)

    # Show the webcam feed
    cv2.imshow("Virtual Presentation Controller", frame)

    # Keyboard controls for the OpenCV window
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('c'):
        annotations = []  # Clear the drawings

cap.release()
cv2.destroyAllWindows()
