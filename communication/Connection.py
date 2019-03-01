import threading
from time import sleep


class Connection(threading.Thread):
    def __init__(self, connection, queue=None, verbose=False, logger=None):
        """if a queue is given the messages will be stored in it
        if verbose is True, the messages will be printed
        if a logger is given the messages will be logged in it"""
        threading.Thread.__init__(self)
        self.connection = connection
        self.instruction_list = queue
        self.is_open = True
        self.last_message_received = None
        self.verbose = verbose
        self.logger = logger

        self.kill_buffer = 0
        self.kill_threshold = 20

    def run(self):
        """an infinite loop which wait for new messages"""
        while True:
            # self.receive()

            try:
                self.receive()

                self.kill_buffer = 0
            except:
                sleep(0.5)

                if self.logger:
                    self.logger.error("error in reception")

                self.kill_buffer += 1

                if self.kill_buffer>self.kill_threshold:
                    self.connection.close()
                    break

        self.is_open = False

    def receive(self):
        message = self.connection.recv()
        self.last_message_received = message

        if self.instruction_list:
            self.instruction_list.put((message, self.connection))
            # print(message)
        else:
            if self.verbose:
                # used for client side connections
                print(message)

        # if self.logger:
        #     self.logger.error("MESSAGE RECEIVED: " + message)
