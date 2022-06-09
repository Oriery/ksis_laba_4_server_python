import asyncio
import websockets
import json
import random
import string

USERS = set()
usernames = {}


async def addUser(websocket):
    USERS.add(websocket)

    usernames[websocket] = generateRandomNickname()


def generateRandomNickname():
    random_username = randomword(4) + str(random.randint(1000, 9999))
    while (random_username in usernames.values()):
        random_username = randomword(4) + str(random.randint(1000, 9999))

    return random_username


async def removeUser(websocket):
    USERS.remove(websocket)
    usernames.pop(websocket)


def makeMessage(message, websocket):
    return json.dumps({'nickname': usernames[websocket], 'message': message})


async def socket(websocket, path):
    await addUser(websocket)

    try:
        while True:
            message = await websocket.recv()

            await asyncio.wait([user.send(makeMessage(message, websocket)) for user in USERS])
    finally:
        await removeUser(websocket)


def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


start_server = websockets.serve(socket, '127.0.0.1', 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
