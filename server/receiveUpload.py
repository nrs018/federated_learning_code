import socket
import pandas as pd
import os
import tqdm
import time
from itertools import chain
import netifaces as ni

class receiveUpload():
    def __init__(self):
        self.uploadPort = 40002
        self.currentTime = None

    def setTime(self, t):
        self.currentTime = t

    def receiveUploadModel(self):
        s = socket.socket()
        ip = ni.ifaddresses('wlo1')[ni.AF_INET][0]['addr']
        s.bind((ip, self.uploadPort))
        s.listen(100)
        connection, address = s.accept()
        # print(address[0])
        f = open('./model/' + str(address[0]) + '.pt', 'wb')
        totalsize = 0
        data = connection.recv(1024)
        while data:
            f.write(data)
            data = connection.recv(1024)
            totalsize += data.__len__()
        f.close()
        connection.close()
        print('received local model from ', address[0], ', consumed time:', time.time() - self.currentTime)
