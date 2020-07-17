import cv2
import json
from datetime import datetime

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Cannot open camera")

events = []


def write_to_file():
    with open('results/face_detection_results.json', 'w') as file:
        json_str = json.dumps(events, indent=4)
        file.write(json_str)


wasFaceLastIteration = False

while True:
    # Capture frames
    ret, frame = cap.read()

    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame. Exiting ...")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) != 0:
        if not wasFaceLastIteration:
            events.append((datetime.now().isoformat(), 'I see you'))
            write_to_file()
            wasFaceLastIteration = True
    else:
        if wasFaceLastIteration:
            events.append((datetime.now().isoformat(), 'I don\'t see you'))
            write_to_file()
            wasFaceLastIteration = False

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

    cv2.imshow('img', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
