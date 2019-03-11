#!/usr/bin/env python

# WS server that sends messages at random intervals

import asyncio
import websockets


async def broadcast(web_socket, path):
    while True:
        await web_socket.send('hello')
        await asyncio.sleep(0.5)


async def main(web_socket, path):
    await asyncio.wait([
        broadcast(web_socket, path),
        receive(web_socket, path)
    ])


async def receive(web_socket, path):
    while True:
        message = await web_socket.recv()
        print(message)


start_server = websockets.serve(main, '127.0.0.1', 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
