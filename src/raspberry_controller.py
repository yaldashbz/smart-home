# Import essential libraries
from time import sleep

import cv2
import numpy as np
import requests

from client import ClientSocket


def process(response):
    # finger count
    if state == 1:
        print(f"response in finger COUNT is {response}")

    # mnist sign language
    if state == 2:
        print(f"response in MNIST is {response}")

    # volume
    if state == 3:
        print(f"VOLUME is {response}")


# Replace the below URL with your own. Make sure to add "/shot.jpg" at last.

url = "http://192.168.212.20:8080/shot.jpg"
TCP_IP = 'localhost'
TCP_PORT = 8081
client = ClientSocket(TCP_IP, TCP_PORT)

reset = True
state = 0  #  0 1 2 3

# While loop to continuously fetching data from the Url
while True:
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)
    img = cv2.resize(img, (640, 480))
    cv2.imshow("Android_cam", img)
    client.sendImages(img, state)

    print(f"reset is {reset}")
    print(f"state is {state}")
    response = client.sock.recv(4).decode()
    reset = int(response[-1])
    print(f'received state in client is {str(state)}')
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
    sleep(10)

cv2.destroyAllWindows()
