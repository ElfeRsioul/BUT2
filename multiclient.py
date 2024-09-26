import socket
import os
from _thread import *

ClientSocket = None
host = '127.0.0.1'
port = 9090
myNumber = 0

def main():
    ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        ClientSocket.connect((host, port))

    except socket.error as e:
        print(str(e))

    finally:
        print("connected to Server !")
        myNumber = int(ClientSocket.recv(1024))
        print("myNumber client received : ", myNumber)
        start_new_thread(threaded_server, (ClientSocket, myNumber))

while True:
    msg = input('') # bloquant les retours => nécessite un thread
    ClientSocket.send(str.encode(msg))
    if msg == "quit": # Bogue sur le quit !
        ClientSocket.send(str.encode(str(myNumber)))
    break

def threaded_server(connection, num):
    while True:
        response = connection.recv(1024)
        print(response.decode('utf-8'))


if __name__== "__main__":
    main()