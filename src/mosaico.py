# coding=utf-8
from PIL import Image
import os
from .MinHeap import Heap
from .AVL import AVLTree
import random

# Dado un color promedio, regresa la ruta de la imagen cuyo color promedio es el más cercano a ese color.
def getClosestImage (RGB,tree):
    epsilon = 2
    # Las imagenes más cercanas
    nearest_points = tree.getNearestPoints(formatt(RGB,epsilon))
    # Si no encontramos nada, ampliamos el rango de búsqueda.
    while not nearest_points or len(nearest_points) < 5: # Podría ser longitud < 2.
        # Duplicamos el tamaño.
        epsilon *= 2
        nearest_points = tree.getNearestPoints(formatt(RGB,epsilon))
    points = []
    for i in range(len(nearest_points)):
        # Los colores
        RGB2 = nearest_points[i][:-2]
        # La ruta
        name = nearest_points[i][-2]
        img = nearest_points[i][-1]
        # Sacamos la distancia del punto actual, con el que buscamos.
        distance = getDistance(RGB,RGB2)
        points.append([distance,name,img])
    # Metemos los puntos a un montículo mínimo
    heap = Heap(points)
    # Lo regresamos a lista y regresamos los primeros n elementos (los mejores.)
    return heap.getNSmallest()

# Dados dos colores en RGB regresa su distancia.
def getDistance (RGB1,RGB2):
    r1,g1,b1 = RGB1
    r2,g2,b2= RGB2 
    # Distancia euclideana.
    distancia = (((r1-r2)**2)+((g1-g2)**2)+((b1-b2)**2))**(.5)

    return distancia

# Dados dos colores en RGB, determina si son iguales.
def sameColor(RGB1,RGB2):
    return RGB1 == RGB2

# Para poder realizar las búsquedas en el árbol de rangos, le damos formato a RGB.
# epsilon será para ampliar la búsqueda en el árbol; por default será uno.
def formatt (RGB,epsilon=1):
    
    R = [RGB[0] - epsilon , RGB[0] + epsilon]
    G = [RGB[1] - epsilon , RGB[1] + epsilon]
    B = [RGB[2] - epsilon , RGB[2] + epsilon]

    return (R,G,B)

# Dada una imágen, y el tamaño del mosaico crea el foto mosaico.
# La guarda con el nombre que recibe (name).
def filtroMosaico(imagen,tree,mosaic_size):
    # Variables auxiliares.
    recorreX = 0
    recorreY = 0
    rprom = 0
    gprom = 0
    bprom = 0
    prom = 0
    ancho = imagen.size[0]
    alto = imagen.size[1]
    rgb = imagen.convert('RGB')
    pixels = imagen.load()
    old_RGB = []

    # La imagen que será el mosaico.
    new_im = Image.new('RGB', (ancho, alto))

    for i in range(0,ancho,mosaic_size):
        recorreX = i + mosaic_size

        for j in range(0,alto,mosaic_size):
            recorreY = j + mosaic_size

            for k in range(i,recorreX):
                if (k >= ancho):
                    break

                for l in range(j,recorreY):
                    if (l >= alto):
                        break

                    r,g,b = rgb.getpixel((k,l))
                    rprom += r
                    gprom += g
                    bprom += b
                    prom += 1

            # El color promedio de la región cuadrada.
            promRojo = (rprom/prom)
            promVerde = (gprom/prom)
            promAzul = (bprom/prom)

            # Reseteamos valores.
            rprom = 0
            gprom = 0
            bprom = 0
            prom = 0

            # Empieza lo bueno.
            RGB = (promRojo,promVerde,promAzul)
            # Si el pixel de hace rato es distinto al de 
            if not sameColor(old_RGB,RGB):
                # Actualizamos el valor del nuevo color
                old_RGB = RGB
                # Regresa el arreglo con las imágenes más cercanas.
                heap = getClosestImage(RGB,tree)
            # Elegimos una posición aleatoria de nuestro arreglo.
            index = random.randint(0,3) # len(heap)-1)
            # Lo pegamos al mosaico
            img = heap[index][2]
            new_im.paste(img, (i,j))

    path = "./src/result.jpg"
    new_im.save(path)

    return new_im

def process_image (img, tree,mosaic_size):
    mosaico = filtroMosaico(img,tree,mosaic_size)
    return mosaico
