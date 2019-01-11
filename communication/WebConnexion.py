from multiprocessing.connection import Listener
from time import sleep

port = 6001

address = ('127.0.0.1', port)  # family is deduced to be 'AF_INET'
listener = Listener(address)


connexion = listener.accept()
print('connection accepted from', listener.last_accepted)
print('1')

while True:
    try:
        msg = connexion.recv()
        print(msg)
    except:
        connexion.close()
        print('new')
        sleep(1)

    # do something with msg


# listener.close()
