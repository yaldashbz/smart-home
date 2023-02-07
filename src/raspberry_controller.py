# Import essential libraries
from time import sleep

import cv2
import numpy as np
import requests

from client import ClientSocket
from led import turn_on_led, turn_off_led

"""
Controller script to run on raspberry pi
"""

def process(response):
    # finger count
    if state == 1:
        if response in [0, 1]:
            turn_off_led(1)
        print("response in finger COUNT is ", response)
        if response in [4, 5]:
            turn_on_led(5, 1, 1)

    # mnist sign language
    if state == 2:
        if response in range(10):
            turn_on_led(2, 1, 2)
        if response in range(10, 20):
            turn_on_led(2, 1, 4)
        if response in range(20, 26):
            turn_on_led(2, 1, 6)
        print("response in MNIST is ", response)

    # volume
    if state == 3:
        turn_on_led(response // 10, 1, 1)
        print("VOLUME is ", response)


# Replace the below URL with your own. Make sure to add "/shot.jpg" at last.

url = "http://192.168.1.100:8080/shot.jpg"
TCP_IP = '192.168.212.104'
TCP_PORT = 12397
client = ClientSocket(TCP_IP, TCP_PORT)

reset = True
state = 0  # 0 1 2 3

# While loop to continuously fetching data from the Url
while True:
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)
    img = cv2.resize(img, (640, 480))
    cv2.imshow("Android_cam", img)
    client.sendImages(img, state)

    print("reset is ", reset)
    print("state is ", state)
    response = client.sock.recv(4).decode()
    reset = int(response[-1])
    print('received state in client is', str(state))
    if reset:
        state = 0
    else:
        res = int(response[:-1])
        process(res)
        if state == 0:
            state = res
        reset = 0

    print('-' * 30)
    # Press Esc key to exit
    if cv2.waitKey(1) == 27:
        break
    sleep(1)

cv2.destroyAllWindows()
