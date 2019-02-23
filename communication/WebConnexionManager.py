import threading
from multiprocessing.connection import Listener
import communication.Connexion as Connexion
import queue


class WebConnexionManager(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.address = ('localhost', 6003)  # family is deduced to be 'AF_INET'
        try:
            self.listener = Listener(self.address, authkey=b'secret password')
        except:
            self.address = ('localhost', 6004)  # family is deduced to be 'AF_INET'
            self.listener = Listener(self.address, authkey=b'secret password')
        self.web_connexions_queue_list = []
        self.web_connexions_list = []

    def run(self):
        """an infinite loop which wait for new connections"""
        print("[WEB_CONNEXION_MANAGER] start connecting")
        while True:
            self.connexion_init()

    def connexion_init(self):
        new_connexion = self.listener.accept()
        new_connexion_queue = queue.Queue()

        new_connexion_thread = Connexion.Connexion(new_connexion, new_connexion_queue)
        new_connexion_thread.daemon = True

        new_connexion_thread.start()
        self.web_connexions_queue_list.append(new_connexion_queue)
        self.web_connexions_list.append(new_connexion_thread)
        print('[WEB_CONNEXION_MANAGER] connexion accepted from', self.listener.last_accepted)
