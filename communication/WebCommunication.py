#!/usr/bin/env python3

import asyncio
import websockets
from threading import Thread


class WebCommunication(Thread):
    def __init__(self, ip, port):
        """ip is the host ip [str]
        port is the port of the socket [integer]"""
        Thread.__init__(self)
        self.ip = ip
        self.port = port

    def run(self):
        print("[WEB COMMUNICATION] starting")
        self.server = websockets.serve(self.communicate, self.ip, self.port)
        asyncio.get_event_loop().run_until_complete(self.server)
        asyncio.get_event_loop().run_forever()

    async def communicate(self, web_socket, path):
        await asyncio.wait([
            self.broadcast(web_socket, path),
            self.receive(web_socket, path)
        ])

    async def broadcast(self, web_socket, path):
        while True:
            await web_socket.send('hello from rasp')
            await asyncio.sleep(0.5)

    async def receive(self, web_socket, path):
        while True:
            message = await web_socket.recv()
            print("[WEB COMMUNICATION] message received : " + message)


w = WebCommunication('10.57.167.107', 5678)
w.daemon = True
w.start()
input()
