"""
Agus Teira
Div K
"""

import pygame
from constantes import *

def getSuperficies(path: str,filas: int, columnas:int)->list:
    lista=[]
    superficie_imagen = pygame.image.load(path)
    fotograma_ancho = int(superficie_imagen.get_width()/columnas)
    fotograma_alto = int(superficie_imagen.get_height()/filas)

    for columna in range(columnas):
        for fila in range(filas):
            x = columna * fotograma_ancho
            y = fila * fotograma_alto
            #un pedacito de la imagen del sprite
            superficie_fotograma = superficie_imagen.subsurface(x,y,fotograma_ancho, fotograma_alto)
            lista.append(superficie_fotograma)

    return lista

def reproducir_musica(ruta,canal):
    cancion = pygame.mixer.Sound(ruta)  # Cargar el archivo de música
    numero_cancion = pygame.mixer.Channel(canal)

    if canal == 0:
        numero_cancion.play(cancion, loops=-1)
    elif canal == 1:
        numero_cancion.set_volume(0.1)
        numero_cancion.play(cancion)
    elif canal == 2:
        numero_cancion.set_volume(0.2)
        numero_cancion.play(cancion)
    return numero_cancion

def crear_enemigos(Enemigo:object ,screen,cantidad:int, distancia:int, tamaño:int, vida:int)->list:
    enemigos1 = []
    pixeles = 120
    for i in range(cantidad):
        pixeles += distancia
        enemigo = Enemigo(tamaño, vida)
        enemigo.rect.x = pixeles
        enemigo.dibujar(screen)
        enemigos1.append(enemigo)
    return enemigos1

