import ConnexionWaiter


class Receiver:
    def __init__(self):
        self.connexion_waiter = ConnexionWaiter.ConnexionWaiter()
        self.connexion_waiter.start()

    def receive(self):
        for connexion in self.connexion_waiter.connexions_list:
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
