import socket
import netifaces as ni
import tqdm
import os
import time

class uploadModel():
    def __init__(self):
        self.serverIP = '192.168.192.60'
        self.uploadPort = 40002
        self.filename = './model/globalModel.pt'
        self.filesize = os.path.getsize(self.filename)

    def uploadModel(self):
        f = open('./model/localModel.pt', 'rb')

        s = socket.socket()
        s.connect((self.serverIP, self.uploadPort))
        with tqdm.tqdm(range(self.filesize)) as progress:
            time.sleep(0.1)
            progress.set_description('uploading model to ' + self.serverIP)
            while True:
                data = f.read(1024)
                if not data:
                    break
                s.sendall(data)
                progress.update(data.__len__())
        s.close()
