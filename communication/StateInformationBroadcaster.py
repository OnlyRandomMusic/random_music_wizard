# aims at sending information to all client side connection in the form of a dictionary
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
                self.broadcast(self.feedback_receiver.receiver.connection_manager.connections_list, state_information)
                self.broadcast(self.feedback_receiver.receiver.web_connection_manager.web_connections_list, state_information)

            sleep(0.5)

    def broadcast(self, connections, information):
        for connection in connections:
            if connection.is_open:
                try:
                    connection.connection.send(information)
                except:
                    continue

    def monitor_state(self):
        if self.feedback_receiver.music_wizard:
            if self.feedback_receiver.music_wizard.player:
                return self.feedback_receiver.music_wizard.player.get_current_music_info()
