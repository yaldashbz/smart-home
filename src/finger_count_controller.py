from collections import Counter

import cv2

from utils import find_position, find_landmark


class FingerCountController:
    """
    Count up fingers
    """
    def __init__(self):
        self.tip = [8, 12, 16, 20]
        self.tipname = [8, 12, 16, 20]

    def process(self, img):
        finger, fingers = list(), list()
        frame1 = cv2.resize(img, (640, 480))
        frame1 = frame1.copy()

        a = find_position(frame1)
        b = find_landmark(frame1)
        if len(b and a) != 0:
            finger = []
            if a[0][1:] < a[4][1:]:
                finger.append(1)
            else:
                finger.append(0)

            fingers = []
            for idx in range(0, 4):
                if a[self.tip[idx]][2:] < a[self.tip[idx] - 2][2:]:
                    fingers.append(1)
                else:
                    fingers.append(0)

        x = fingers + finger
        c = Counter(x)
        up = c[1]

        cv2.imshow("Frame", frame1)
        key = cv2.waitKey(1) & 0xFF

        return up
