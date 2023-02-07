import base64
import socket
import threading

import cv2
import numpy

from finger_count_controller import FingerCountController
from sign_language_controller import SignLanguageController
from utils import find_landmark
from volume_controller import VolumeController

count_controller = FingerCountController()
sign_controller = SignLanguageController()
volume_controller = VolumeController()

CONTROLLERS = [
    count_controller,
    sign_controller,
    volume_controller
]


class ServerSocket:
    """
    Server Socket class for handling processing recived image from client, base on state
    """
    def __init__(self, ip, port):
        self.TCP_IP = ip
        self.TCP_PORT = port
        self.socketOpen()
        self.receiveThread = threading.Thread(target=self.receiveImages)
        self.receiveThread.start()

    def socketClose(self):
        self.sock.close()
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is close')

    def socketOpen(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.TCP_IP, self.TCP_PORT))
        self.sock.listen(1)
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is open')
        self.conn, self.addr = self.sock.accept()
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(
            self.TCP_PORT) + ' ] is connected with client')

    def receiveImages(self):
        try:
            while True:
                length = self.recvall(self.conn, 64)
                length1 = length.decode('utf-8')
                stringData = self.recvall(self.conn, int(length1))
                stime = self.recvall(self.conn, 64)
                state = int(self.recvall(self.conn, 64))
                # print('send time: ' + stime.decode('utf-8'))
                # print('receive time: ' + datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f'))
                data = numpy.frombuffer(base64.b64decode(stringData), numpy.uint8)
                decimg = cv2.imdecode(data, 1)
                reset = len(find_landmark(decimg)) == 0
                if reset:
                    print("RESET, Hand Not detected!")
                    self.conn.send(str(0).encode())
                else:
                    if state == 0:
                        state = 1
                    state = state if 1 <= state <= 3 else 1
                    print("CONTROLLER state in server is ", state)
                    res = CONTROLLERS[state - 1].process(decimg)
                    print("Res in server ", res)
                    self.conn.send(str(res).encode())
                # reset
                self.conn.send(str(int(reset)).encode())
                print('-' * 30)
        except Exception as e:
            print(e)
            self.socketClose()
            cv2.destroyAllWindows()
            self.socketOpen()
            self.receiveThread = threading.Thread(target=self.receiveImages)
            self.receiveThread.start()

    def recvall(self, sock, count):
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf


def main():
    TCP_IP = '192.168.212.104'
    TCP_PORT = 12397
    ServerSocket(TCP_IP, TCP_PORT)


if __name__ == "__main__":
    main()
