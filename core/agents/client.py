import socket
import sys
import os
import asyncio
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)

from crypto.aes_encryptor import AESEncryptor
from commands.crocodilec import crocodile

class AsyncClient:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port

    async def connect(self):
        reader, writer = await asyncio.open_connection(self.host, self.port)
        session_id = await reader.read(36)  # Suponiendo que el servidor envía un UUID
        session_id = session_id.decode().strip()
        print(f"Sesión iniciada con ID: {session_id}")
        
        asyncio.create_task(self.listen_server(reader))  # Hilo asíncrono para recibir mensajes
        
        while True:
            message = input("Mensaje al servidor: ")
            writer.write(message.encode())
            await writer.drain()

    async def listen_server(self, reader):
        while True:
            data = await reader.read(1024)
            if not data:
                print("Desconectado del servidor.")
                break
            print(f"Servidor: {data.decode().strip()}")

if __name__ == "__main__":
    client = AsyncClient()
    asyncio.run(client.connect())
