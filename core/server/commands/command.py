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

    async def start(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):  # ✅ StreamWriter
        if not isinstance(reader, asyncio.StreamReader):
            raise TypeError("reader debe ser una instancia de asyncio.StreamReader")
        # resp = await reader.read(36)
        while True:
            try: 
                command =  await self.get_input("#>: ")
                #await asyncio.to_thread(input, resp.decode("utf-8", errors="replace") + " ")
                r = command.encode('utf-8')
                writer.write(r)
                # writer.drain()
                resp = await reader.read(36)  # ✅ Esperar respuesta del cliente
                if not resp:
                    print("🔴 El cliente cerró la conexión.")
                    break
                    
                print("Respuesta recibida:", resp.decode("utf-8", errors="replace"))
            except Exception as e:
                print("ocurrio un error", e)
        # encrypt = self.encryptor.encrypt(comand.decode())
        # await writer.drain()
        # # print(f"Enviado: {encrypt}")
        
        # res = await reader.read(4096)
        # if res:
        #     print(res.decode())
            # decrypted_response = await self.encryptor.decrypt(res)
            # agent_id, command = await self.process_check_in(decrypted_response)
            # print(agent_id, command.decode())
    async def get_input(self,prompt: str):
        return await asyncio.to_thread(input, prompt)
    async def process_check_in(self, data: str) -> tuple:
        """Procesa el check-in de un agente."""
        agent_id, metadata = data.split("|")
        self.sessions[agent_id] = metadata
        return agent_id, "collect_info"
