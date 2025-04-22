# core/crypto.py
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
class AESEncryptor:
    def __init__(self, key: bytes):
        if len(key) not in [16, 24, 32]:
            raise ValueError(f"Clave AES inválida: {len(key)} bytes. Debe ser 16, 24 o 32 bytes.")
        self.key = key

    def encrypt(self, plaintext: str) -> bytes:
        try:
            nonce = os.urandom(12)
            cipher = Cipher(algorithms.AES(self.key), modes.GCM(nonce), backend=default_backend())
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
            return nonce + encryptor.tag + ciphertext
        except Exception as e:
                print(e)
         
    def decrypt(self, data: str) -> str:
        try:
            raw_data = data  # Decodifica el Base64
            nonce, tag, ciphertext = raw_data[:12], raw_data[12:28], raw_data[28:]

            cipher = Cipher(algorithms.AES(self.key), modes.GCM(nonce, tag), backend=default_backend())
            decryptor = cipher.decryptor()
            plaintext = decryptor.update(ciphertext) + decryptor.finalize()

            return plaintext
        except Exception as e:
            print(f"Error en descifrado: {e}")
            return None
        
    def encryptBytes(self, plaintext: str) -> bytes:
        try:
            nonce = os.urandom(12)
            cipher = Cipher(algorithms.AES(self.key), modes.GCM(nonce), backend=default_backend())
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(plaintext) + encryptor.finalize()
            return nonce + encryptor.tag + ciphertext
        except Exception as e:
                print(e)