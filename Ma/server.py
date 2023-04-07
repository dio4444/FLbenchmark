from socket import *

backlog = 10
buffsize = 1024
server = socket(AF_INET, SOCK_STREAM)
server.bind(("127.0.0.1", 5666))
server.listen(backlog)
clientsocket, clientaddr = server.accept()
while True:
    msg = clientsocket.recv(buffsize)
    print('client msg:', msg.decode('utf-8'))
    clientsocket.sendall(input('your msg:').encode('utf-8'))
