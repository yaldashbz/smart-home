from time import sleep

import cv2

from volume_controller import VolumeController

cap = cv2.VideoCapture(0)

controller = VolumeController()
while True:
    success, img = cap.read()
    controller.process(img)
    sleep(1)
