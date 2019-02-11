import threading


class Connexion(threading.Thread):
    def __init__(self, connexion, queue=None):
        threading.Thread.__init__(self)
        self.connexion = connexion
        self.instruction_list = queue

    def run(self):
        """an infinite loop which wait for new messages"""
        while True:
            try:
                message = self.connexion.recv()

                # if message == 'get':
                #     self.connexion.send('je suis là')

                if self.instruction_list:
                    self.instruction_list.put((message, self.connexion))
                    # print(message)
                else:
                    # used for client side connexions
                    print(message)
            except:
                self.connexion.close()
