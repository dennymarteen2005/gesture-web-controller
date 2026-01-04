import cv2
import mediapipe as mp
import time
import pyautogui

# ---------------- CONFIG ----------------

HOLD_TIME = 1.0
MODE_HOLD_TIME = 3.0
ACTION_DELAY = 1.2

MODE = "WEB"   # WEB or PPT

last_action_time = 0
gesture_start_time = None
mode_start_time = None
last_detected_gesture = None

# ---------------- MEDIAPIPE ----------------

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8
)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# ---------------- HELPERS ----------------

def safe_action():
    global last_action_time
    if time.time() - last_action_time > ACTION_DELAY:
        last_action_time = time.time()
        return True
    return False


def is_thumb_open(hand, label):
    if label == "Right":
        return hand.landmark[4].x < hand.landmark[3].x
    return hand.landmark[4].x > hand.landmark[3].x


def finger_states(hand, label):
    fingers = []
    fingers.append(1 if is_thumb_open(hand, label) else 0)
    for tip in [8, 12, 16, 20]:
        fingers.append(1 if hand.landmark[tip].y < hand.landmark[tip - 2].y else 0)
    return fingers


# ---------------- MAIN LOOP ----------------

print("🎮 Gesture Controller | WEB works WITHOUT extension | Q to exit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    detected_gesture = None
    display_text = f"MODE: {MODE}"

    if result.multi_hand_landmarks and result.multi_handedness:
        for hand, handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
            label = handedness.classification[0].label
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            thumb, index, middle, ring, pinky = finger_states(hand, label)

            # -------- MODE SWITCH (3 FINGERS HOLD) --------
            if index == middle == ring == 1 and thumb == pinky == 0:
                if mode_start_time is None:
                    mode_start_time = time.time()
                elif time.time() - mode_start_time >= MODE_HOLD_TIME:
                    MODE = "PPT" if MODE == "WEB" else "WEB"
                    print("MODE CHANGED TO:", MODE)
                    mode_start_time = None
                    time.sleep(0.5)
            else:
                mode_start_time = None

            # -------- PLAY / PAUSE (COMMON) --------
            if thumb == 1 and index == middle == ring == pinky == 0:
                detected_gesture = "PLAY_PAUSE"
                display_text = "👍 PLAY / PAUSE"

            # -------- WEB MODE --------
            elif MODE == "WEB":
                if index == 1 and middle == 1 and thumb == ring == pinky == 0:
                    detected_gesture = "SCROLL_DOWN"
                    display_text = "✌️ SCROLL DOWN"

                elif index == 1 and thumb == middle == ring == pinky == 0:
                    detected_gesture = "PREV"
                    display_text = "☝️ PREVIOUS"

                elif index == 1 and pinky == 1 and thumb == middle == ring == 0:
                    detected_gesture = "NEXT"
                    display_text = "🤘 NEXT"

            # -------- PPT MODE --------
            elif MODE == "PPT":
                if index == 1 and middle == 1 and thumb == ring == pinky == 0:
                    detected_gesture = "NEXT_SLIDE"
                    display_text = "✌️ NEXT SLIDE"

                elif index == 1 and thumb == middle == ring == pinky == 0:
                    detected_gesture = "PREV_SLIDE"
                    display_text = "☝️ PREVIOUS SLIDE"

            # -------- EXECUTION --------
            if detected_gesture == last_detected_gesture:
                if gesture_start_time is None:
                    gesture_start_time = time.time()
                elif time.time() - gesture_start_time >= HOLD_TIME and safe_action():

                    if MODE == "WEB":
                        if detected_gesture == "PLAY_PAUSE":
                            pyautogui.press("space")
                        elif detected_gesture == "SCROLL_DOWN":
                            pyautogui.scroll(-500)
                        elif detected_gesture == "PREV":
                            pyautogui.hotkey("shift", "p")  # YouTube prev
                        elif detected_gesture == "NEXT":
                            pyautogui.hotkey("shift", "n")  # YouTube next

                    elif MODE == "PPT":
                        if detected_gesture == "PLAY_PAUSE":
                            pyautogui.press("space")
                        elif detected_gesture == "NEXT_SLIDE":
                            pyautogui.press("right")
                        elif detected_gesture == "PREV_SLIDE":
                            pyautogui.press("left")

                    gesture_start_time = None
                    last_detected_gesture = None
            else:
                gesture_start_time = None

            last_detected_gesture = detected_gesture

            cv2.putText(frame, display_text, (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Gesture Controller (NO EXTENSION)", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
