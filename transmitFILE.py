import socket
import sys
import time
# 路径有四中：当前路径，data文件夹，model文件，src文件
def main(argv):

    f = open(argv[2], 'rb')

    s = socket.socket()
    s.connect(('192.168.192.27', 40003))
    s.send(bytes(argv[1], encoding='utf-8'))
    time.sleep(5)
    data = f.read(1024)
    while data:
        s.sendall(data)
        data = f.read(1024)
    s.close()

if __name__ == '__main__':
    main(sys.argv)
