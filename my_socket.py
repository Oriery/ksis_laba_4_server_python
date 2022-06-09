import asyncio
import websockets

USERS = set()

async def addUser(websocket):
    USERS.add(websocket)

async def removeUser(websocket):
    USERS.remove(websocket)

async def socket(websocket, path):
    await addUser(websocket)
    print(len(USERS), USERS)

start_server = websockets.serve(socket, '127.0.0.1', 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()