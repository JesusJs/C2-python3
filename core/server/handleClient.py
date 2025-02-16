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
        print(f"🎮 Nueva sesión [{session_id}] desde {addr} :")

    async def access_session(self, session_id, message):
        async with self.lock:
            session = self.sessions.get(session_id)
            if session:
                writer = session["writer"]
                reader = session['reader']
                try:
                    await self.shell.start(reader, writer)
                except (BrokenPipeError, ConnectionResetError):
                    print(f"Cliente {session_id} desconectado.")
                    self.sessions.pop(session_id, None)
            else:
                print(f"Sesión {session_id} no encontrada")
            