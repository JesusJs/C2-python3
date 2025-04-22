import os
import requests

def getImageAndSave():
    response = requests.get('https://urra.com.co/wp-content/uploads/2021/02/Todo-lo-que-debe-saber-sobre-la-factura-de-energia-electrica-CREG.pdf')
    if( response.status_code == 200):

        with open("pdf.pdf", "wb") as file:
                file.write(response.content)
    else:
        print(f"Error al descargar la imagen: {response.status_code}")    

    os.startfile('pdf.pdf')

getImageAndSave()