import threading
from multiprocessing.connection import Listener
import Connexion


class ConnexionManager(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.address = ('localhost', 6000)  # family is deduced to be 'AF_INET'
        self.listener = Listener(self.address, authkey=b'secret password')
        self.connexions_list = []

    def run(self):
        """an infinite loop which wait for new connections"""
        print("[RASP] start connecting")
        while True:
            self.connexion_init()

    def connexion_init(self):
        new_connexion = self.listener.accept()
        new_connexion_thread = Connexion.Connexion(new_connexion)
        new_connexion_thread.start()
        self.connexions_list.append(new_connexion_thread)
        print('[RASP] connexion accepted from', self.listener.last_accepted)


c = ConnexionManager()
c.start()
