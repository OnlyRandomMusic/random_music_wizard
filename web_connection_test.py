# coding: utf-8

import socket
from time import sleep

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('', 15559))

socket.listen(5)
client, address = socket.accept()
print("{} connected".format( address ))

while True:
    response = client.recv(255)
    message = str(response, 'utf8')

    if message != '':
        print(message)

    if message == 'close':
        break


print("Close")
client.close()
socket.close()
