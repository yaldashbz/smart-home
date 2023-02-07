import base64
import socket
import sys
import time
from datetime import datetime

import cv2
import numpy


class ClientSocket:
    """
    Client Socket class for handling connection to server and sending images to it.
    """

    def __init__(self, ip, port):
        self.TCP_SERVER_IP = ip
        self.TCP_SERVER_PORT = port
        self.connectCount = 0
        self.connectServer()

    def connectServer(self):
        try:
            self.sock = socket.socket()
            self.sock.connect((self.TCP_SERVER_IP, self.TCP_SERVER_PORT))
            print(
                u'Client socket is connected with Server socket [ TCP_SERVER_IP: ' + self.TCP_SERVER_IP + ', TCP_SERVER_PORT: ' + str(
                    self.TCP_SERVER_PORT) + ' ]')
            self.connectCount = 0
        except Exception as e:
            print(e)
            self.connectCount += 1
            if self.connectCount == 10:
                print(u'Connect fail %d times. exit program' % (self.connectCount))
                sys.exit()
            print(u'%d times try to connect with server' % (self.connectCount))
            self.connectServer()

    def sendImages(self, frame, state=1):
        cnt = 0
        try:
            resize_frame = cv2.resize(frame, dsize=(480, 315), interpolation=cv2.INTER_AREA)
            stime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
            result, imgencode = cv2.imencode('.jpg', resize_frame, encode_param)
            data = numpy.array(imgencode)
            stringData = base64.b64encode(data)
            length = str(len(stringData))
            self.sock.sendall(length.encode('utf-8').ljust(64))
            self.sock.send(stringData)
            self.sock.send(stime.encode('utf-8').ljust(64))
            self.sock.send(str(state).encode('utf-8').ljust(64))
            # print(u'send images %d' % (cnt))
            cnt += 1
            time.sleep(1)
        except Exception as e:
            print(e)
            self.sock.close()
            time.sleep(1)
            self.connectServer()
            self.sendImages(frame)

    def recvall(self, sock, count):
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf


def main():
    TCP_IP = 'localhost'
    TCP_PORT = 8081
    ClientSocket(TCP_IP, TCP_PORT)


if __name__ == '__main__':
    main()
