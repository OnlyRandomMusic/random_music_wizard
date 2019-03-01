from multiprocessing.connection import Client
from communication import Connexion


class ServerClient:
    # the server side connexion object
    def __init__(self, logger):
        self.logger = logger
        self.connexion = None
        self.message_receiver = None

        self.logger.error("server_client connected")

    def connect(self):
        """connect the server script to the feedback receiver
        return False if the server didn't manage to connect the feedback receiver"""

        # need to use the message_receiver.is_open

        if not self.connexion:
            self.logger.error("trying to open a new connexion")
            try:
                address = ('localhost', 6003)
                new_connexion = Client(address, authkey=b'secret password')
            except:
                try:
                    address = ('localhost', 6004)
                    new_connexion = Client(address, authkey=b'secret password')
                except:
                    return False

            self.logger.error("new connexion open")

            self.connexion = new_connexion

            self.message_receiver = Connexion.Connexion(new_connexion, logger=self.logger)
            self.message_receiver.daemon = True
            self.message_receiver.start()
        else:
            self.logger.error("connexion already open")

        return True

    def send(self, message):
        self.logger.error("message sent: " + message)
        self.connexion.send(message)

    def get_title(self):
        if self.message_receiver:
            if self.message_receiver.last_message_received:
                return self.message_receiver.last_message_received
            return 'no song currently playing'
        return 'no connexion'
