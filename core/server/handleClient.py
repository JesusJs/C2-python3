import uuid
import asyncio
import threading
from commands.command import Crocodile

class HandleClient:
    def __init__(self, sessions):
        self.sessions = sessions
        self.lock = asyncio.Lock()
        self.shell = Crocodile()

    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info("peername")
        session_id = str(uuid.uuid4())
        
        async with self.lock:
            self.sessions[session_id] = {"reader": reader, "writer": writer, "address": addr}
        
        print(f"🎮 Nueva sesión [{session_id}] desde {addr}")
        
        writer.write(f"SESSION_ID:{session_id}\n".encode())
        await writer.drain()
        
        try:
            while data := await reader.read(1024):
                message = data.decode().strip()
                print(f"🔹 Mensaje recibido de {addr}: {message}")
                writer.write(b"ACK\n")
                await writer.drain()
        except asyncio.CancelledError:
            print(f"Cliente {addr} desconectado.")
        finally:
            async with self.lock:
                self.sessions.pop(session_id, None)

    async def access_session(self, session_id, message):
        async with self.lock:
            session = self.sessions.get(session_id)
            if session:
                writer = session["writer"]
                reader = session["reader"]
                try:
                    writer.write(message.encode() + b"\n")
                    await writer.drain()
                    print(f"Mensaje enviado a la sesión {session_id}")
                except (BrokenPipeError, ConnectionResetError):
                    print(f"Cliente {session_id} desconectado.")
                    self.sessions.pop(session_id, None)
            else:
                print(f"Sesión {session_id} no encontrada")