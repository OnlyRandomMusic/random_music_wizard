import threading
from time import sleep


class Connexion(threading.Thread):
    def __init__(self, connexion, queue=None, verbose=False, logger=None):
        """if a queue is given the messages will be stored in it
        if verbose is True, the messages will be printed
        if a logger is given the messages will be logged in it"""
        threading.Thread.__init__(self)
        self.connexion = connexion
        self.instruction_list = queue
        self.is_open = True
        self.last_message_received = None
        self.verbose = verbose
        self.logger = logger

    def run(self):
        """an infinite loop which wait for new messages"""
        while True:
            try:
                message = self.connexion.recv()
                self.last_message_received = message

                if self.instruction_list:
                    self.instruction_list.put((message, self.connexion))
                    # print(message)
                else:
                    if self.verbose:
                        # used for client side connexions
                        print(message)

                if self.logger:
                    self.logger.error("MESSAGE RECEIVED: " + message)
            except:
                sleep(0.5)
                # self.connexion.close()
                # break

        self.is_open = False
