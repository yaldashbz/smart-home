# Import essential libraries
from time import sleep

import cv2
import numpy as np
import requests

from client import ClientSocket

# Replace the below URL with your own. Make sure to add "/shot.jpg" at last.

url = "http://192.168.183.9:8080/shot.jpg"
TCP_IP = 'localhost'
TCP_PORT = 8081
client = ClientSocket(TCP_IP, TCP_PORT)

# While loop to continuously fetching data from the Url
while True:
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)
    img = cv2.resize(img, (640, 480))
    cv2.imshow("Android_cam", img)
    client.sendImages(img)
    res = client.sock.recv(4)
    print('resssssssssss in client ', str(res))
    # client.recvall(client.sock, 4)

    # Press Esc key to exit
    if cv2.waitKey(1) == 27:
        break

    sleep(10)

cv2.destroyAllWindows()
