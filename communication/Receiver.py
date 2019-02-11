import communication.ConnexionManager as ConnexionManager
import communication.WebConnexionManager as WebConnexionManager
from time import sleep


class Receiver:
    def __init__(self, instruction_queue):
        self.connexion_manager = ConnexionManager.ConnexionManager()
        self.connexion_manager.daemon = True

        self.web_connexion_manager = WebConnexionManager.WebConnexionManager()
        self.web_connexion_manager.daemon = True

        self.connexion_manager.start()
        self.web_connexion_manager.start()
        self.instruction_queue = instruction_queue

        print("[RECEIVER] receiver initialized")

    def receive(self):
        # receiving messages from ssh connexions
        for connexion_queue in self.connexion_manager.connexions_list:
            try:
                if connexion_queue.qsize() > 0:
                    instruction = connexion_queue.get()
                    self.instruction_queue.put(instruction)
                    print("[RECEIVER] ssh instruction received: " + instruction)
            except:
                print("[RECEIVER] error in ssh reception")
                continue

        # receiving messages from web connexions
        for web_connexion_queue in self.web_connexion_manager.web_connexions_list:
            if web_connexion_queue.qsize() > 0:
                instruction = web_connexion_queue.get()
                self.instruction_queue.put(instruction)

            # try:
            #     if web_connexion_queue.qsize() > 0:
            #         instruction = web_connexion_queue.get()
            #         self.instruction_queue.put(instruction)
            #         print("[RECEIVER] web instruction received: " + instruction)
            # except:
            #     print("[RECEIVER] error in web reception")
            #     continue

# receiver = Receiver(1)
#
# while True:
#     receiver.receive()
#     sleep(1)
