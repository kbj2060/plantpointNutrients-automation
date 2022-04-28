import websockets
from config import SOCKET_HOST


async def send_socket(data: dict):
    ws = await websockets.connect(SOCKET_HOST, ping_timeout=None, ping_interval=None)
    await ws.send(data)

async def send_ping():
    ws = await websockets.connect(SOCKET_HOST, ping_timeout=None, ping_interval=None)
    await ws.ping()