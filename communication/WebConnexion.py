import threading


class WebConnexion(threading.Thread):
    def __init__(self, connexion, queue):
        threading.Thread.__init__(self)
        self.connexion = connexion
        self.instruction_list = queue

    def run(self):
        """an infinite loop which wait for new messages"""
        while True:
            try:
                message = self.connexion.recv()
                print(message)
                self.instruction_list.put(message)
            except:
                self.connexion.close()

