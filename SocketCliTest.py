from socket import *

cliSock = socket(AF_INET, SOCK_STREAM)
cliSock.connect(('localhost', 9091))

while True:
    data1 = input('>')

    if not data1:
        break

    cliSock.send(data1.encode())
    data1 = cliSock.recv(1024)

    if not data1:
        break
    print(data1.decode('utf-8'))

cliSock.close()