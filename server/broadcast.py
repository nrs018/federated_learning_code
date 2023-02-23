import socket
import pandas as pd
import os
import tqdm
import time
from itertools import chain

class broadcastModel():
    def __init__(self):
        self.client_ip = []
        self.BroadcastPort = 40001
        self.filename = './model/globalModel.pt'
        self.filesize = os.path.getsize(self.filename)
        tmp = pd.read_csv('./client_ip_list.txt').values.tolist()
        self.client_ip = chain.from_iterable(tmp)

    def broadcastmodel(self):
        f = open(self.filename, 'rb')
        s = socket.socket()
        for clientIP in self.client_ip:
            start_Broadcast = time.time()
            print(clientIP)
            s.connect((clientIP, 40001))
            with tqdm.tqdm(range(self.filesize)) as progress:
                time.sleep(0.1)
                progress.set_description("Broadcasting global model to " + clientIP)
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    s.sendall(data)
                    progress.update(data.__len__())

            print('broadcast model to ', clientIP, 'consumedTime = ', time.time() - start_Broadcast,
                  ', throughput:{:3.2f}'.format(self.filesize / ((time.time() - start_Broadcast) * 1024 * 1024)))
        s.close()


#