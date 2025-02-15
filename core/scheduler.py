import threading
import asyncio
from handleClient import HandleClient

class Server:
    def __init__(self):
        self.sessions = {}
        self.handler = HandleClient(self.sessions)

    async def start_server(self, host='127.0.0.1', port=65432):
        server = await asyncio.start_server(self.handler.handle_client, host, port)
        print(f"🟢 Servidor iniciado en {host}:{port}")
        
        await asyncio.gather(
            server.serve_forever(),
            self.server_admin_interface()
        )

    async def server_admin_interface(self):
        while True:
            command = await asyncio.to_thread(input, "Comando del servidor (SEND <session_id>): ")
            if command.startswith("SEND"):
                parts = command.split(maxsplit=2)
                if len(parts) < 3:
                    print("Formato: SEND <session_id> <mensaje>")
                    continue
                _, session_id, message = parts
                await self.handler.access_session(session_id, message)

if __name__ == "__main__":
    asyncio.run(Server().start_server())
    