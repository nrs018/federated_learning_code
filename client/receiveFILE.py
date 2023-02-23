import socket
import netifaces as ni

s = socket.socket()
# get local host ip address
ip = ni.ifaddresses('wlp3s0')[ni.AF_INET][0]['addr']
s.bind((ip, 40003))
s.listen(1)
connection, address = s.accept()
path_file = connection.recv(1024).decode('utf-8')
# print('transmitting ', path_file, ', wait for five seconds...')

# connection, address = s.accept()
f = open(path_file, 'wb')

data = connection.recv(1024)

while data:
   f.write(data)
   data = connection.recv(1024)

f.close()
connection.close()

