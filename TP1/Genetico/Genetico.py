import os
import sys
import csv
import random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from TP1.Busqueda_Global.BG_Tablero import Tablero
from TP1.Genetico.Gen_TempleSimulado import TempleSimulado
import pygame

archivo = "TP1/Genetico/ordenes.csv"
archivo_poblacion = "TP1/Genetico/poblacion.csv"

PASILLO = 0
ESTANTE = 1
DESCARGA = 2

hc = 30
wc = 30

class Celda():
    def __init__(self, tipo, pos):
        self.tipo = tipo
        self.tipo_ant = -1
        self.ocupado = False
        self.vecinos: Celda = []
        self.pos = pos
        self.visitado = 0

    def get_color(self):
        if self.visitado and self.tipo == ESTANTE:
            return (0, self.visitado*100, 100)
        if self.tipo == PASILLO:
            return (255, 0, 100)
        elif self.tipo == ESTANTE:
            return (0, 0, 100)
        elif self.tipo == DESCARGA:
            return (62, 91, 88)
            
class Estante(Celda):
    contador_id = 0
    def __init__(self,pos):
        super().__init__(ESTANTE,pos)
        Estante.contador_id += 1
        self.id = Estante.contador_id

class Mapa():
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.celdas = [[Celda(PASILLO, (i, j)) for j in range(alto)] for i in range(ancho)]
        self.estantes = []

    def agregar_estantes(self, x, y, ancho, alto):
        for i in range(x, x+ancho):
            for j in range(y, y+alto):
                self.celdas[i][j] = Estante((i, j))
                self.celdas[i][j].ocupado = True
                self.estantes.append(self.celdas[i][j])

    def dibujar(self, pantalla):
        for i in range(self.ancho):
            for j in range(self.alto):
                color = pygame.Color(0, 0, 0)
                color.hsva = self.celdas[i][j].get_color()
                pygame.draw.rect(pantalla, color, (i*wc+1, j*hc+1, wc-2, hc-2))
                if self.celdas[i][j].tipo == ESTANTE:
                    font = pygame.font.Font(None, 20)
                    text = font.render(str(self.celdas[i][j].id), True, (0, 0, 0))
                    pantalla.blit(text, (i*wc+10, j*hc+10))
                self.celdas[i][j].tipo_ant = self.celdas[i][j].tipo

mapa=Mapa(13, 11)
mapa.agregar_estantes(2, 1, 2, 4)
mapa.agregar_estantes(2, 6, 2, 4)
mapa.agregar_estantes(6, 1, 2, 4)
mapa.agregar_estantes(6, 6, 2, 4)
mapa.agregar_estantes(10, 1, 2, 4)
mapa.agregar_estantes(10, 6, 2, 4)
mapa.celdas[0][5].tipo = DESCARGA


#defino al tablero
tablero = Tablero(11, 13)

def idoneidad(individuos):
    for individuo in individuos:
        ordenesIndividuo = []
        for orden in ordenes:
            ordenAux = []
            for i in orden:
                ordenAux.append(individuo[0][i-1])
            ordenesIndividuo.append(ordenAux)
            #Ordenes hijo, tiene la reorganizacion de todas las ordenes para ese hijo (ese individuo)

        for orden in ordenesIndividuo:
            _,costo,_,_=TempleSimulado(tablero, orden).simular()
            individuo[1] += costo
    suma = 0
    for individuo in individuos:
        suma += individuo[1]
    for individuo in individuos:
        individuo[1] = 1 - individuo[1]/suma
    individuos.sort(key=lambda x: x[1], reverse=True)
    return individuos

ordenes = []
with open(archivo, newline='') as csvfile:
    lector = csv.reader(csvfile)
    for fila in lector:
        ordenes.append([int(producto) for producto in fila])

poblacion = []
# Creacion de la poblacion Inicial
with open(archivo_poblacion, mode='r') as archivo_csv:
    lector = csv.reader(archivo_csv)
    for fila in lector:
        # Convertir cada fila de strings a una lista de enteros
        individuo = list(map(int, fila))
        poblacion.append([individuo,0])



def PMX(padre1, padre2):
    size = len(padre1)
    
    # Seleccionar dos puntos de cruce aleatorios
    punto1 = random.randint(0, size - 2)
    punto2 = random.randint(punto1 + 1, size - 1)
    
    # Inicializar el hijo como lista vacía
    hijo = [None] * size
    hijo[punto1:punto2] = padre1[punto1:punto2]

    # Mapear los genes del padre2 al padre1
    for i in range(punto1, punto2):
        if padre2[i] not in hijo:
            # Si el gen en padre2 no está en el segmento mapeado
            # entonces mapear el gen a la posición correspondiente
            # en padre1
            idx = padre2.index(padre1[i])
            while hijo[idx] is not None:
                idx = padre2.index(padre1[idx])
            hijo[idx] = padre2[i]
    for i in range(size):
        if hijo[i] is None:
            hijo[i] = padre2[i]
    return hijo

def mutar(poblacion):
    for individuo in poblacion:
        if random.random() < 0.5:
            cantidad_mutaciones = random.randint(5, 10)
            for _ in range(cantidad_mutaciones):
                idx1 = random.randint(0, len(individuo[0]) - 1)
                idx2 = random.randint(0, len(individuo[0]) - 1)
                individuo[0][idx1], individuo[0][idx2] = individuo[0][idx2], individuo[0][idx1]
    return poblacion

def reproducir(poblacion):
    pesos = [34, 30, 25, 20]
    lista_padres = poblacion.copy()
    poblacion = poblacion[:2]
    while len(poblacion) < 10:
        padres = random.choices(lista_padres, weights=[pesos[i] for i in range(4)], k=2)
        iter=0
        while padres[0] == padres[1]:
            iter+=1
            padres = random.choices(lista_padres, weights=[pesos[i] for i in range(4)], k=2)
            if iter>10:
                break
        iter=0
        while padres[0] == padres[1]:
            iter+=1
            padres = mutar(padres)
            if iter>10:
                break
        hijo = PMX(padres[0][0], padres[1][0])
        saltear = False
        for individuo in poblacion:
            if individuo[0] == hijo:
                saltear = True
                break
        if saltear:
            continue
        poblacion.append([hijo, 0])
    return poblacion

def plotear_mejor(poblacion):
    mejor_individuo = poblacion[0]
    ordenesIndividuo = []
    ordenes_por_estante = [0 for i in range(1, 49)]
    for orden in ordenes:
        ordenAux = []
        for i in orden:
            ordenAux.append(mejor_individuo[0][i-1])
        ordenesIndividuo.append(ordenAux)
    for orden in ordenesIndividuo:
        for i in orden:
            ordenes_por_estante[i-1] += 1

    ordenes_por_estante = [x / max(ordenes_por_estante) for x in ordenes_por_estante]
    for estante in mapa.estantes:
        estante.visitado = ordenes_por_estante[estante.id-1]

poblacion = poblacion[:4]

for i in range(100):
    poblacion = reproducir(poblacion)
    poblacion = mutar(poblacion)
    poblacion = idoneidad(poblacion)[:4]
    plotear_mejor(poblacion)
    pygame.init()
    pantalla = pygame.display.set_mode((13*wc, 11*hc))
    mapa.dibujar(pantalla)
    pygame.display.flip()
    pygame.time.wait(1000)
    pygame.image.save(pantalla, "captura"+str(i)+".png")
    pygame.time.wait(1000)
    pygame.quit()


