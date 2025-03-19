import os
import pygame
import heapq
import random as rd

# Establecer la variable de entorno para centrar la ventana
os.environ['SDL_VIDEO_CENTERED'] = '1'

PASILLO = 0
ESTANTE = 1
DESCARGA = 2
V1 = 3
M1 = 4
M2 = 5
M3 = 6
M4 = 7

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
        if self.visitado and self.tipo == PASILLO:
            if self.visitado == 2:
                return (183, 30, 88)
        if self.tipo == PASILLO:
            return (255, 0, 100)
        elif self.tipo == ESTANTE:
            return (0, 100, 0)
        elif self.tipo == DESCARGA:
            return (62, 91, 88)            
        elif self.tipo == M1:
            return (200, 100, 88)
        elif self.tipo == M2:
            return (20, 100, 88)
        elif self.tipo == M3:
            return (150, 100, 88)
        elif self.tipo == M4:
            return (100, 100, 88)
        
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
        for i in range(ancho):
            for j in range(alto):
                if i > 0:
                    self.celdas[i][j].vecinos.append(self.celdas[i-1][j])
                if i < ancho-1:
                    self.celdas[i][j].vecinos.append(self.celdas[i+1][j])
                if j > 0:
                    self.celdas[i][j].vecinos.append(self.celdas[i][j-1])
                if j < alto-1:
                    self.celdas[i][j].vecinos.append(self.celdas[i][j+1])
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
                if self.celdas[i][j].tipo != self.celdas[i][j].tipo_ant:
                    color = pygame.Color(0, 0, 0)
                    color.hsva = self.celdas[i][j].get_color()
                    pygame.draw.rect(pantalla, color, (i*wc+1, j*hc+1, wc-2, hc-2))
                    if self.celdas[i][j].tipo == ESTANTE:
                        font = pygame.font.Font(None, 20)
                        text = font.render(str(self.celdas[i][j].id), True, (255, 255, 255))
                        pantalla.blit(text, (i*wc+10, j*hc+10))
                    self.celdas[i][j].tipo_ant = self.celdas[i][j].tipo

    def encontrar_camino(self, inicio, objetivo):
        def heuristica(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        abiertos = []
        heapq.heappush(abiertos, (0, inicio))
        padres = {inicio: None}
        costos = {inicio: 0}

        while abiertos:
            _, actual = heapq.heappop(abiertos)

            if actual == objetivo:
                camino = []
                while actual:
                    camino.append(actual)
                    actual = padres[actual]
                return camino[::-1]

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = actual[0] + dx, actual[1] + dy
                if 0 <= nx < self.ancho and 0 <= ny < self.alto:
                    vecino = (nx, ny)
                    if not self.celdas[nx][ny].ocupado:
                        nuevo_costo = costos[actual] + 1
                        if vecino not in costos or nuevo_costo < costos[vecino]:
                            costos[vecino] = nuevo_costo
                            prioridad = nuevo_costo + heuristica(vecino, objetivo)
                            heapq.heappush(abiertos, (prioridad, vecino))
                            padres[vecino] = actual

        return None
    def ir_al_estante(self, inicio, estante):#recibe el id del estante
        celda_estante = self.estantes[estante-1]
        celda_adyacente = None
        if celda_estante.pos[0] > 0 and not self.celdas[celda_estante.pos[0]-1][celda_estante.pos[1]].tipo == ESTANTE:
            celda_adyacente = self.celdas[celda_estante.pos[0]-1][celda_estante.pos[1]]
        elif celda_estante.pos[0] < self.ancho-1 and not self.celdas[celda_estante.pos[0]+1][celda_estante.pos[1]].tipo == ESTANTE:
            celda_adyacente = self.celdas[celda_estante.pos[0]+1][celda_estante.pos[1]]
        objetivo = celda_adyacente.pos
        camino = self.encontrar_camino(inicio, objetivo)
        return camino
        

pygame.init()

pantalla = pygame.display.set_mode((13*wc, 11*hc))
mapa = Mapa(13, 11)
mapa.agregar_estantes(2, 1, 2, 4)
mapa.agregar_estantes(2, 6, 2, 4)
mapa.agregar_estantes(6, 1, 2, 4)
mapa.agregar_estantes(6, 6, 2, 4)
mapa.agregar_estantes(10, 1, 2, 4)
mapa.agregar_estantes(10, 6, 2, 4)
mapa.celdas[0][5].tipo = DESCARGA
mapa.celdas[0][5].ocupado = True
mapa.dibujar(pantalla)
pygame.display.flip()

#tasks=[(pos_inicial),estante]
tasks=[]
tasks.append([(0,5),41,M1])
tasks.append([(12,5),20,M2])
tasks.append([(12,0),4,M3])
tasks.append([(0,10),35,M4])
#caminos=[[pos_anterior,[camino],estante]]
caminos=[]
for task in tasks:
    camino=mapa.ir_al_estante(task[0],task[1])
    caminos.append([None,camino,task[1],task[2]])
pygame.time.wait(10000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    for camino in caminos:
        if not camino[1]:
            caminos.remove(camino)
            continue
        celda = camino[1][0]
        if camino[0]:
            alternativo=mapa.ir_al_estante(camino[0].pos, camino[2])
            if alternativo:
                alternativo.pop(0)
                if len(alternativo)<len(camino[1]):
                    camino[1] = alternativo
                    celda = camino[1][0]
        if mapa.celdas[celda[0]][celda[1]].ocupado and mapa.celdas[celda[0]][celda[1]].tipo != DESCARGA:
            nuevo_camino = mapa.ir_al_estante(camino[0].pos, camino[2])
            if nuevo_camino == None:
                continue
            camino[1] = nuevo_camino
            camino[1].pop(0)
            celda = camino[1][0]
        if camino[0]:
            camino[0].tipo = PASILLO
            camino[0].visitado = 2
            camino[0].ocupado = False
        camino[0] = mapa.celdas[celda[0]][celda[1]]
        mapa.celdas[celda[0]][celda[1]].tipo = camino[3]
        mapa.celdas[celda[0]][celda[1]].ocupado = True
        mapa.dibujar(pantalla)
        pygame.display.flip()
        pygame.time.wait(200)
        camino[1].pop(0)