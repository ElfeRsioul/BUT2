import socket
import os
from _thread import *


ServerSocket = None
host = '127.0.0.1'
port = 9090
clients = []
nbclients = 0
numclient = None


def main():
    global nbclients
    ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        ServerSocket.bind((host, port))

    except socket.error as e:
        print(str(e))
        
    finally:
        print('Waiting for a Connection..')
        ServerSocket.listen(5)


    while True:
        client, address = ServerSocket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        client.send(str.encode(str(nbclients)))
        clients.append(client)
        print("Liste clients : ", clients)
        start_new_thread(threaded_client, (client, ))
        nbclients+=1
        print('Thread Number: ' + str(nbclients))

def threaded_client(connection):
    global nbclients
    print("connection", connection)

    while True:

        data = connection.recv(2048)
        reply = '\n>>' + data.decode('utf-8') + '\n'
        for client in clients:
            client.sendall(str.encode(reply))
        if data == "quit": # Bogue sur le quit !
            numclient = int(connection.recv(2048))
            clients[numclient].close()
            clients.pop(numclient)
            nbclients-=1

if __name__== "__main__":
    main()