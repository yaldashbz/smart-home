import cv2
import mediapipe as freedomtech

drawer = freedomtech.solutions.drawing_utils
hands_recognizer = freedomtech.solutions.hands

mod = hands_recognizer.Hands()

h = 480
w = 640


def find_position(frame):
    positions = []
    results = mod.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    if results.multi_hand_landmarks is not None:
        for mark in results.multi_hand_landmarks:
            drawer.draw_landmarks(frame, mark, hands_recognizer.HAND_CONNECTIONS)
            for idx, pt in enumerate(mark.landmark):
                x = int(pt.x * w)
                y = int(pt.y * h)
                positions.append([idx, x, y])

    return positions


def find_landmark(frame1):
    landmarks = []
    results = mod.process(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))
    if results.multi_hand_landmarks is not None:
        for _ in results.multi_hand_landmarks:
            for point in hands_recognizer.HandLandmark:
                landmarks.append(
                    str(point).replace("< ", "").replace("HandLandmark.", "").replace("_", " ").replace("[]", ""))
    return landmarks
