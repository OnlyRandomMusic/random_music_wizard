from multiprocessing.connection import Client

address = ('localhost', 6000)
conn = Client(address, authkey=b'secret password')

while True:
    message = input()

    if message == 'quit':
        break

    conn.send(message)


conn.close()
