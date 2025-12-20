import cv2
import mediapipe as mp
import pyautogui
import time

# ---------------- SETUP ----------------

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8
)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

HOLD_TIME = 1.0
MODE_HOLD_TIME = 1.5
ACTION_DELAY = 1.2
SCROLL_AMOUNT = 600

last_action_time = 0
gesture_start_time = None
mode_start_time = None
last_detected_gesture = None

MODE = "PPT"   # PPT or WEB


# ---------------- HAND LOGIC ----------------

def is_thumb_open(hand_landmarks, hand_label):
    if hand_label == "Right":
        return hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x
    else:
        return hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x


def finger_states(hand_landmarks, hand_label):
    fingers = []
    fingers.append(1 if is_thumb_open(hand_landmarks, hand_label) else 0)
    for tip in [8, 12, 16, 20]:
        fingers.append(
            1 if hand_landmarks.landmark[tip].y <
            hand_landmarks.landmark[tip - 2].y else 0
        )
    return fingers  # [thumb, index, middle, ring, pinky]


# ---------------- ACTION HELPERS ----------------

def press_key(key):
    global last_action_time
    now = time.time()
    if now - last_action_time > ACTION_DELAY:
        pyautogui.press(key)
        last_action_time = now


def scroll_up():
    pyautogui.scroll(SCROLL_AMOUNT)


def scroll_down():
    pyautogui.scroll(-SCROLL_AMOUNT)


# ---------------- MAIN LOOP ----------------

print("🎮 Gesture Controller with MODE SWITCH — Press Q to exit")

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
        for hand_landmarks, handedness in zip(
            result.multi_hand_landmarks, result.multi_handedness
        ):
            hand_label = handedness.classification[0].label
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            thumb, index, middle, ring, pinky = finger_states(hand_landmarks, hand_label)

            # -------- MODE SWITCH (DOUBLE FIST) --------
            if thumb == index == middle == ring == pinky == 0:
                if mode_start_time is None:
                    mode_start_time = time.time()
                elif time.time() - mode_start_time >= MODE_HOLD_TIME:
                    MODE = "WEB" if MODE == "PPT" else "PPT"
                    print("MODE CHANGED TO:", MODE)
                    mode_start_time = None
                    last_action_time = time.time()
            else:
                mode_start_time = None

            # -------- GESTURES --------
            if MODE == "PPT":
                if thumb == 1 and index == middle == ring == pinky == 0:
                    detected_gesture = "PLAY"
                    display_text = "👍 PLAY / PAUSE"
                elif index == 1 and middle == 1 and ring == pinky == thumb == 0:
                    detected_gesture = "NEXT"
                    display_text = "✌️ NEXT SLIDE"
                elif thumb == index == middle == ring == pinky == 1:
                    detected_gesture = "PREVIOUS"
                    display_text = "✋ PREVIOUS SLIDE"
                elif index == 1 and middle == ring == pinky == thumb == 0:
                    detected_gesture = "FIRST"
                    display_text = "☝️ FIRST SLIDE"
                elif index == middle == ring == pinky == 1 and thumb == 0:
                    detected_gesture = "LAST"
                    display_text = "🤘 LAST SLIDE"

            elif MODE == "WEB":
                if index == 1 and middle == 1 and ring == pinky == thumb == 0:
                    detected_gesture = "SCROLL_DOWN"
                    display_text = "✌️ SCROLL DOWN"
                elif thumb == index == middle == ring == pinky == 1:
                    detected_gesture = "SCROLL_UP"
                    display_text = "✋ SCROLL UP"

            # -------- HOLD CONFIRM --------
            if detected_gesture == last_detected_gesture:
                if gesture_start_time is None:
                    gesture_start_time = time.time()
                elif time.time() - gesture_start_time >= HOLD_TIME:
                    if detected_gesture == "PLAY":
                        press_key("space")
                    elif detected_gesture == "NEXT":
                        press_key("right")
                    elif detected_gesture == "PREVIOUS":
                        press_key("left")
                    elif detected_gesture == "FIRST":
                        press_key("home")
                    elif detected_gesture == "LAST":
                        press_key("end")
                    elif detected_gesture == "SCROLL_DOWN":
                        scroll_down()
                    elif detected_gesture == "SCROLL_UP":
                        scroll_up()

                    gesture_start_time = None
                    last_detected_gesture = None
            else:
                gesture_start_time = None

            last_detected_gesture = detected_gesture

            cv2.putText(
                frame,
                display_text,
                (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

    cv2.imshow("Gesture Controller (Mode Switch)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
