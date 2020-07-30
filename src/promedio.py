# coding=utf-8
from cloudinary.api import resources
from PIL import Image
import requests
from io import BytesIO
import os



# Obtiene el promedio general de (R,G,B) de toda la imagen.
def getPromedioRGB(img):
    # Los futuros promedios
    r_prom = 0
    g_prom = 0
    b_prom = 0
    total = 0
    # Accedemos a la matriz de pixeles de ambas imagenes.
    pixeles = None
    try:
        pixeles = img.load()
    except Exception as e:
        print(e)
        return None
    # Iteramos sobre cada pixel y comparamos.
    try:
        for i in range(0,img.size[0]):
            for j in range(0,img.size[1]):
                r,g,b = pixeles[i,j]
                r_prom += r
                g_prom += g
                b_prom += b
                total += 1
    except Exception as e:
        return None
    
    # Lo divimos para que sea el promedio
    r_prom = r_prom//total
    g_prom = g_prom//total
    b_prom = b_prom//total

    # Lo regresamos en forma de cadena
    return str(r_prom) + ","+ str(g_prom) + ","+ str(b_prom)

# Itera sobre la carpeta con imágenes para obtener su color promedio.
def getPromedios (path):
    f = open("./src/BD.txt","w+")
    # Una ""Base de Datos"" para guardar el nombre de la imagen y su color promedio en RGB.
    for filename in os.listdir(path):
        if filename.endswith(".jpg") or filename.endswith(".JPG") or filename.endswith(".png") or filename.endswith(".jpeg"):
            im = None
            try:
                im = Image.open(path + filename)
            except Exception as e:
                continue
            
            prom = getPromedioRGB(im) 
            if prom:    
                f.write(path + filename + "," + prom  + "\n")
        elif os.path.isdir(path + filename):
            print("Directorio actual: " + filename)
            getPromedios(path + filename + "/")
    f.close()

def fill_db():

    f = open("./src/BD.txt","w+")
    response = resources(type = "upload", max_results=5000)
    
    for item in response.get("resources"):

        if item.get("bytes", 0) > 0:

            img = None

            try:
                img_bytes = requests.get(item.get("url"))
                img = Image.open(BytesIO(img_bytes.content))
            except Exception as e:
                continue

            prom = getPromedioRGB(img)

            if prom:    
                f.write(
                    f'{item.get("url")},{prom}\n'
                )
    
    f.close()
