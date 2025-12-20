import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ ERROR: Camera not accessible")
    exit()

print("✅ Camera opened successfully")

while True:
    ret, frame = cap.read()

    if not ret:
        print("❌ ERROR: Failed to read frame")
        break

    cv2.imshow("Webcam Live Feed - Press Q to Exit", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
