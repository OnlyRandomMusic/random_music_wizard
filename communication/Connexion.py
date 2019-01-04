import threading


class Connexion(threading.Thread):
    def __init__(self, connexion):
        threading.Thread.__init__(self)
        self.connexion = connexion

    def run(self):
        """an infinite loop which wait for new messages"""
        while True:
            try:
                msg = self.connexion.recv()
                print(msg)
            except:
                self.connexion.close()
