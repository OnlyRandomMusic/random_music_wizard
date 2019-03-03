import threading
from multiprocessing.connection import Listener
import communication.Connection as Connection
import queue


class WebConnectionManager(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.address = ('localhost', 6003)  # family is deduced to be 'AF_INET'
        try:
            self.listener = Listener(self.address, authkey=b'secret password')
        except:
            self.address = ('localhost', 6004)  # family is deduced to be 'AF_INET'
            self.listener = Listener(self.address, authkey=b'secret password')
        self.web_connections_queue_list = []
        self.web_connections_list = []

    def run(self):
        """an infinite loop which wait for new connections"""
        print("[WEB_CONNECTION_MANAGER] start connecting")
        while True:
            self.connection_init()

    def connection_init(self):
        new_connection = self.listener.accept()
        new_connection_queue = queue.Queue()

        new_connection_thread = Connection.Connection(new_connection, new_connection_queue)
        new_connection_thread.daemon = True

        new_connection_thread.start()
        self.web_connections_queue_list.append(new_connection_queue)
        self.web_connections_list.append(new_connection_thread)
        print('[WEB_CONNECTION_MANAGER] connection accepted from', self.listener.last_accepted)
