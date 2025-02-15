# core/crypto.py
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import asyncio
class AESEncryptor:
    def __init__(self, key: bytes):
        if len(key) not in [16, 24, 32]:
            raise ValueError(f"Clave AES inválida: {len(key)} bytes. Debe ser 16, 24 o 32 bytes.")
        self.key = key

    def encrypt(self, plaintext: str) -> bytes:
        nonce = os.urandom(12)
        cipher = Cipher(algorithms.AES(self.key), modes.GCM(nonce), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
        return nonce + encryptor.tag + ciphertext
         
    async def decrypt(self, data: str) -> str:
        nonce, tag, ciphertext = data[:12], data[12:28], data[28:]
        cipher = await Cipher(algorithms.AES(self.key), modes.GCM(nonce, tag), backend=default_backend())
        decryptor = await cipher.decryptor()
        fynalD = ""
        if(decryptor):
            fynalD = decryptor.update(ciphertext)
        return fynalD