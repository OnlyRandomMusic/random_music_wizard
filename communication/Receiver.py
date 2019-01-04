import ConnexionManager


class Receiver:
    def __init__(self):
        self.connexion_manager = ConnexionManager.ConnexionManager()
        self.connexion_manager.start()

    def receive(self):
        for connexion in self.connexion_manager.connexions_list:
            try:
                msg = connexion.recv()
                print(msg)
            except:
                connexion.close()


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
