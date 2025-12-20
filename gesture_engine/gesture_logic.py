import cv2
import mediapipe as mp

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)


def is_thumb_open(hand_landmarks, hand_label):
    if hand_label == "Right":
        return hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x
    else:
        return hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x


def are_other_fingers_closed(hand_landmarks):
    return (
        hand_landmarks.landmark[8].y > hand_landmarks.landmark[6].y and
        hand_landmarks.landmark[12].y > hand_landmarks.landmark[10].y and
        hand_landmarks.landmark[16].y > hand_landmarks.landmark[14].y and
        hand_landmarks.landmark[20].y > hand_landmarks.landmark[18].y
    )


def detect_thumbs_up(hand_landmarks, hand_label):
    return is_thumb_open(hand_landmarks, hand_label) and are_other_fingers_closed(hand_landmarks)


def count_fingers(hand_landmarks, hand_label):
    # If thumbs-up detected → force count = 1
    if detect_thumbs_up(hand_landmarks, hand_label):
        return 1

    fingers = []

    # Thumb
    fingers.append(1 if is_thumb_open(hand_landmarks, hand_label) else 0)

    # Other fingers
    for tip in [8, 12, 16, 20]:
        fingers.append(1 if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y else 0)

    return fingers.count(1)


print("✋ Gesture system running... Press Q to exit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks and result.multi_handedness:
        for hand_landmarks, handedness in zip(
            result.multi_hand_landmarks, result.multi_handedness
        ):
            hand_label = handedness.classification[0].label

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            if detect_thumbs_up(hand_landmarks, hand_label):
                gesture = "👍 THUMBS UP"
                finger_count = 1
            else:
                finger_count = count_fingers(hand_landmarks, hand_label)
                gesture = f"FINGERS: {finger_count}"

            cv2.putText(
                frame,
                f"{hand_label} - {gesture}",
                (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

    cv2.imshow("Gesture Detection (Final Fix)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
