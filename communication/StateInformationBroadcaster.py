# aims at sending information to all client side connexion in the form of a dictionary
import threading
from time import sleep


class StateInformationBroadcaster(threading.Thread):
    def __init__(self, feedback_receiver):
        threading.Thread.__init__(self)
        self.feedback_receiver = feedback_receiver

    def run(self):
        while True:
            state_information = self.monitor_state()

            if state_information:
                self.broadcast(self.feedback_receiver.receiver.connexion_manager.connexions_list, state_information)
                self.broadcast(self.feedback_receiver.receiver.web_connexion_manager.web_connexions_list, state_information)

            sleep(0.5)

    def broadcast(self, connexions, information):
        for connexion in connexions:
            connexion.send(information)

    def monitor_state(self):
        if self.feedback_receiver.player:
            return self.feedback_receiver.player.get_current_music_info()
