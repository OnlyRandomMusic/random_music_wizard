import communication.ConnectionManager as ConnectionManager
import communication.WebConnectionManager as WebConnectionManager
from time import sleep


class Receiver:
    def __init__(self, instruction_queue):
        self.connection_manager = ConnectionManager.ConnectionManager()
        self.connection_manager.daemon = True

        self.web_connection_manager = WebConnectionManager.WebConnectionManager()
        self.web_connection_manager.daemon = True

        self.connection_manager.start()
        self.web_connection_manager.start()
        self.instruction_queue = instruction_queue

        print("[RECEIVER] receiver initialized")

    def receive(self):
        # receiving messages from ssh connections
        for connection_queue in self.connection_manager.connections_queue_list:
            try:
                if connection_queue.qsize() > 0:
                    instruction = connection_queue.get()
                    self.instruction_queue.put(instruction)
                    print("[RECEIVER] ssh instruction received: " + instruction[0])
            except:
                print("[RECEIVER] error in ssh reception")
                continue

        # receiving messages from web connections
        for web_connection_queue in self.web_connection_manager.web_connections_queue_list:
            try:
                if web_connection_queue.qsize() > 0:
                    instruction = web_connection_queue.get()
                    self.instruction_queue.put(instruction)
                    print("[RECEIVER] web instruction received: " + instruction[0])
            except:
                print("[RECEIVER] error in web reception")
                continue

# receiver = Receiver(1)
#
# while True:
#     receiver.receive()
#     sleep(1)
