import communication.ConnexionManager as ConnexionManager
from time import sleep


class Receiver:
    def __init__(self, instruction_queue):
        self.connexion_manager = ConnexionManager.ConnexionManager()
        self.connexion_manager.daemon = True

        self.connexion_manager.start()
        self.instruction_queue = instruction_queue

    def receive(self):
        for connexion_queue in self.connexion_manager.connexions_list:
            try:
                if connexion_queue.qsize() > 0:
                    instruction = connexion_queue.get()
                    self.instruction_queue.put(instruction)
                    print("[RASP] instruction received: " + instruction)
            except:
                continue

# receiver = Receiver(1)
#
# while True:
#     receiver.receive()
#     sleep(1)
