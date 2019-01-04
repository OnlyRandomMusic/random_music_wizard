import ConnexionManager
from time import sleep


class Receiver:
    def __init__(self):
        self.connexion_manager = ConnexionManager.ConnexionManager()
        self.connexion_manager.start()

    def receive(self):
        for connexion_queue in self.connexion_manager.connexions_list:
            try:
                if connexion_queue.qsize() > 0:
                    msg = connexion_queue.get()
                    print(msg)
            except:
                continue


# while True:
#     continue
# try:
#     msg = connexion.recv()
#     print(msg)
# except:
#     connexion.close()
#     connexion = connexion_init()
#     print('new')

# do something with msg


# listener.close()

receiver = Receiver()

while True:
    receiver.receive()
    sleep(1)
