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


def prRed(skk): print("\033[91m {}\033[00m".format(skk))


def prGreen(skk): print("\033[92m {}\033[00m".format(skk))


def prYellow(skk): print("\033[93m {}\033[00m".format(skk))


def prLightPurple(skk): print("\033[94m {}\033[00m".format(skk))


def prPurple(skk): print("\033[95m {}\033[00m".format(skk))


def prCyan(skk): print("\033[96m {}\033[00m".format(skk))


def prLightGray(skk): print("\033[97m {}\033[00m".format(skk))