from socket import *

backlog = 10
buffsize = 1024
client = socket(AF_INET, SOCK_STREAM)
client.connect(("127.0.0.1", 5666))
while True:
    client.sendall(input('your msg:').encode('utf-8'))
    print('server msg:', client.recv(buffsize).decode('utf-8'))
