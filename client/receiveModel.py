import socket
import select
import sys
import tqdm
import time
import netifaces as ni


class receiveModel():
    def __init__(self):
        pass

    def receiveBroadcast(self):
        s = socket.socket()
        # get local host ip address
        ip = ni.ifaddresses('wlp3s0')[ni.AF_INET][0]['addr']
        s.bind((ip, 40001))
        s.listen(100)
        rcvData = 0

        connection, address = s.accept()
        f = open('./model/globalModel.pt', 'wb')
        totalsize = 0
        data = connection.recv(1024)
        totalsize += data.__len__()
        while data:
           f.write(data)
           data = connection.recv(1024)
           totalsize += data.__len__()
        f.close()
        connection.close()
        print('global model received from server, the size is ', totalsize)



