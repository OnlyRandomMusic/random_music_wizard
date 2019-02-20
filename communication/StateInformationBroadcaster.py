# aims at sending information to all client side connexion in the form of a dictionary
import threading
from time import sleep


class StateInformationBroadcaster(threading.Thread):
    def __init__(self, connexion_manager, web_connexion_manager):
        threading.Thread.__init__(self)
        self.connexion_list = connexion_manager.connexions_list
        self.web_connexion_list = web_connexion_manager.web_connexions_list

    def run(self):
        while True:
            self.broadcast(self.connexion_list)
            self.broadcast(self.web_connexion_list)
            sleep(0.5)

    def broadcast(self, connexions):
        state_informations = self.monitor_state()

        for connexion in connexions:
            connexion.send(state_informations)

    def monitor_state(self):
        # get title
