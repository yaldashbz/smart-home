import cv2

from finger_count_controller import FingerCountController

cap = cv2.VideoCapture(0)
tip = [8, 12, 16, 20]
tipname = [8, 12, 16, 20]
# fingers = []
# finger = []
controller = FingerCountController()
while True:

    ret, frame = cap.read()
    controller.process(frame)

    # flipped = cv2.flip(frame, flipCode = -1)
    # frame1 = cv2.resize(frame, (640, 480))
    #
    # a = find_position(frame1)
    # b = find_landmark(frame1)
    #
    # if len(b and a) != 0:
    #     finger = []
    #     if a[0][1:] < a[4][1:]:
    #         finger.append(1)
    #         print(b[4])
    #
    #     else:
    #         finger.append(0)
    #
    #     fingers = []
    #     for idx in range(0, 4):
    #         if a[tip[idx]][2:] < a[tip[idx] - 2][2:]:
    #
    #             print(b[tipname[idx]])
    #
    #             # if a[tip[2]] < a[tip[2] - 2]:
    #             #     kit.servo[0].angle = 50
    #
    #             fingers.append(1)
    #
    #         else:
    #             fingers.append(0)
    #
    # x = fingers + finger
    # c = Counter(x)
    # up = c[1]
    # down = c[0]
    # print(up)
    # print(down)
    #
    # cv2.imshow("Frame", frame1)
    # key = cv2.waitKey(1) & 0xFF
    #
    # # My Additions
    # # 5 fingers Up open the door
    # # 0 or `1 close the door
    #
    # if up == 5:
    #     print("Open the door")
    #
    # if up == 1:
    #     print("close the door")
    #
    # if key == ord("q"):
    #     print("you have" + str(up) + "fingers up  and" + str(down) + "fingers down")
    #
    # if key == ord("s"):
    #     break
