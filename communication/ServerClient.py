from multiprocessing.connection import Client
from communication import Connection


class ServerClient:
    # the server side connection object
    def __init__(self, logger):
        self.logger = logger
        self.connection = None
        self.message_receiver = None

        self.logger.error("server_client connected")

    def connect(self):
        """connect the server script to the feedback receiver
        return False if the server didn't manage to connect the feedback receiver"""

        # need to use the message_receiver.is_open

        if not self.connection:
            self.logger.error("trying to open a new connection")
            try:
                address = ('localhost', 6003)
                new_connection = Client(address, authkey=b'secret password')
            except:
                try:
                    address = ('localhost', 6004)
                    new_connection = Client(address, authkey=b'secret password')
                except:
                    return False

            self.logger.error("new connection open")

            self.connection = new_connection

            self.message_receiver = Connection.Connection(new_connection, logger=self.logger)
            self.message_receiver.daemon = True
            self.message_receiver.start()
        else:
            self.logger.error("connection already open")

        return True

    def send(self, message):
        if self.connection:
            self.logger.error("message sent: " + message)
            self.connection.send(message)
        else:
            self.logger.error("no connection available")

    def get_title(self):
        if self.message_receiver:
            if self.message_receiver.last_message_received:
                return self.message_receiver.last_message_received
            return 'no song currently playing'
        return 'no connection'
