from socket import *
from time import ctime

skServer = socket(AF_INET, SOCK_STREAM)
skServer.bind(('localhost', 9091))
skServer.listen(5)


while True:
    clientSocket, addr = skServer.accept()

    while True:
        data = clientSocket.recv(1024)

        if not data:
            break
    
        clientSocket.send(('[%s]%s' % (ctime(), data)).encode())
    clientSocket.close()

skServer.close()
