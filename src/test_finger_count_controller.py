import cv2

from finger_count_controller import FingerCountController

cap = cv2.VideoCapture(0)
controller = FingerCountController()
while True:
    ret, frame = cap.read()
    controller.process(frame)
