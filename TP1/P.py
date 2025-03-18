import os
import pygame

# Establecer la variable de entorno para centrar la ventana
os.environ['SDL_VIDEO_CENTERED'] = '1'

PASILLO = 0
ESTANTE = 1
DESCARGA = 2

hc = 30
wc = 30

class Celda():
    def __init__(self, tipo):
        #tipo puede ser 'pasillo','estante','descarga'
        self.tipo = tipo
        self.ocupado = False
        self.vecinos: Celda = []

    def get_color(self):
        if self.tipo == PASILLO:
            return (255, 0, 100)
        elif self.tipo == ESTANTE:
            return (0, 100, 0)
        elif self.tipo == DESCARGA:
            return (240, 100, 100)

class Estante():
    def __init__(self, id, celda: Celda):
        self.id = id
        self.celda:Celda = celda

class Mapa():
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.celdas = [[Celda(PASILLO) for j in range(alto)] for i in range(ancho)]
        self.estantes = []

    def agregar_estantes(self, x, y, ancho, alto):
        for i in range(x, x+ancho):
            for j in range(y, y+alto):
                self.celdas[i][j].tipo = ESTANTE
                self.estantes.append(self.celdas[i][j])

    def dibujar(self, pantalla):
        # modificar el tamanio de la pantalla segun el mapa
        pantalla = pygame.display.set_mode((self.ancho*wc, self.alto*hc))
        pantalla.fill((0,0,0))
        for i in range(self.ancho):
            for j in range(self.alto):
                color = pygame.Color(0, 0, 0)
                color.hsva = self.celdas[i][j].get_color()
                pygame.draw.rect(pantalla, color, (i*wc+1, j*hc+1, wc-2, hc-2))

pygame.init()

pantalla = pygame.display.set_mode((0,0))
mapa = Mapa(13, 11)
mapa.agregar_estantes(2, 1, 2, 4)
mapa.agregar_estantes(2, 6, 2, 4)
mapa.agregar_estantes(6, 1, 2, 4)
mapa.agregar_estantes(6, 6, 2, 4)
mapa.agregar_estantes(10, 1, 2, 4)
mapa.agregar_estantes(10, 6, 2, 4)
mapa.dibujar(pantalla)
pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()