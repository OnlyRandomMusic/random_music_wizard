import socket

HOST = '10.57.167.107'
PORT = 8484
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(2)

#JS
conn1, addr1 = s.accept()
print('Connected by', addr1)

while 1:
    try:
        print("receiving")
        data = conn1.recv(1024)
        print("received")
    except socket.error:
        print('error')
    if data:
        print(data.decode('utf-8'))
