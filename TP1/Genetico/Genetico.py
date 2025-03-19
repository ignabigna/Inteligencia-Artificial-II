import os
import sys
import csv
import pygame
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from TP1.Busqueda_Global.BG_Tablero import Tablero
from Gen_TempleSimulado import TempleSimulado

archivo = "TP1/Busqueda_Local/ordenes.csv"
ordenes = []
with open(archivo, newline='') as csvfile:
    lector = csv.reader(csvfile)
    for fila in lector:
        ordenes.append([int(producto) for producto in fila])

organizacion = [i for i in range(1, 48)]
tablero = Tablero(11, 13)

'''for orden in ordenes:
    _,costo,_,_=TempleSimulado(tablero, orden).simular()
    print(costo)'''

pygame.init()
pygame.display.set_caption("TP1 - Recolección de pedidos")
pantalla = pygame.display.set_mode((900, 800))
tablero.dibujarTablero(pantalla)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
