import sys
import os
import pygame
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from TP1.Busqueda_Global.BG_Casilla import Casilla
from TP1.Busqueda_Global.BG_AStar import AStar

BLANCO = (255, 255, 255)
AMARILLO = (255, 255, 0)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)

class Tablero:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.tamano_celda = 70
        self.grid = [[Casilla() for _ in range(columnas)] for _ in range(filas)]
        self.posicion = {}
        self.estanterias_cargar()

    def colorear_casilla(self, fila, columna, color):
        if 0 <= fila < self.filas and 0 <= columna < self.columnas:
            self.grid[fila][columna].color = color

    def limpiar_tablero(self):
        for fila in range(self.filas):
            for columna in range(self.columnas):
                casilla = self.grid[fila][columna]
                if casilla.tipo not in ["E", "C"]:
                    casilla.color = BLANCO

    def estanterias_cargar(self):
        estanterias = [
            [(1,2,1), (1,3,2), (2,2,3), (2,3,4), (3,2,5), (3,3,6), (4,2,7), (4,3,8)],
            [(1,6,9), (1,7,10), (2,6,11), (2,7,12), (3,6,13), (3,7,14), (4,6,15), (4,7,16)],
            [(1,10,17), (1,11,18), (2,10,19), (2,11,20), (3,10,21), (3,11,22), (4,10,23), (4,11,24)],
            [(6,2,25), (6,3,26), (7,2,27), (7,3,28), (8,2,29), (8,3,30), (9,2,31), (9,3,32)],
            [(6,6,33), (6,7,34), (7,6,35), (7,7,36), (8,6,37), (8,7,38), (9,6,39), (9,7,40)],
            [(6,10,41), (6,11,42), (7,10,43), (7,11,44), (8,10,45), (8,11,46), (9,10,47), (9,11,48)]
        ]
        
        for grupo in estanterias:
            for fila, columna, numero in grupo:
                self.establecer_casilla(fila, columna, "E", contenido=numero)

        self.establecer_casilla(5, 0, "C")

    def transitable(self, fila, columna):
        if 0 <= fila < self.filas and 0 <= columna < self.columnas:
            return self.grid[fila][columna].tipo in ["R", "C"]
        return False

    def posicion_agente(self, agente, fila, columna):
        if self.transitable(fila, columna) and self.grid[fila][columna].ocupar(agente):
            self.posicion[agente] = (fila, columna)

    def mover_agente(self, agente, nueva_fila, nueva_columna):
        if agente in self.posicion and self.transitable(nueva_fila, nueva_columna):
            fila_actual, columna_actual = self.posicion[agente]
            
            if self.grid[fila_actual][columna_actual].tipo == "A" and self.grid[fila_actual][columna_actual].tipo != "C":
                self.grid[fila_actual][columna_actual].tipo = "R"

            if self.grid[nueva_fila][nueva_columna].tipo != "C":
                self.grid[nueva_fila][nueva_columna].tipo = "A"

            self.posicion[agente] = (nueva_fila, nueva_columna)

    def reiniciar_tablero(self):
        for fila in range(self.filas):
            for columna in range(self.columnas):
                if self.grid[fila][columna].tipo == "A":
                    self.grid[fila][columna].tipo = "R"

    def encontrar_estanteria(self, fila, columna):
        for dx in [-1, 1]:
            nueva_columna = columna + dx
            if self.transitable(fila, nueva_columna):
                return (fila, nueva_columna)
        return None

    def establecer_casilla(self, fila, columna, tipo, contenido=None):
        if 0 <= fila < self.filas and 0 <= columna < self.columnas:
            self.grid[fila][columna] = Casilla(tipo, contenido)

    def dibujar_tablero(self, pantalla):
        fuente = pygame.font.Font(None, 30)
        for fila in range(self.filas):
            for columna in range(self.columnas):
                casilla = self.grid[fila][columna]
                color = self.obtener_color(casilla)
                
                pygame.draw.rect(pantalla, color, (columna * self.tamano_celda, fila * self.tamano_celda, self.tamano_celda, self.tamano_celda))
                pygame.draw.rect(pantalla, NEGRO, (columna * self.tamano_celda, fila * self.tamano_celda, self.tamano_celda, self.tamano_celda), 1)

                self.dibujar_texto_en_casilla(pantalla, casilla, fila, columna, fuente)

    def obtener_color(self, casilla):
        if casilla.tipo == "C":
            return AMARILLO
        elif casilla.tipo == "A":
            return AZUL
        elif casilla.tipo == "E":
            return NEGRO
        elif casilla.tipo == "R":
            return casilla.color
        return BLANCO

    def dibujar_texto_en_casilla(self, pantalla, casilla, fila, columna, fuente):
        if casilla.tipo == "C":
            texto = fuente.render("C", True, NEGRO)
            texto_rect = texto.get_rect(center=(columna * self.tamano_celda + self.tamano_celda // 2, fila * self.tamano_celda + self.tamano_celda // 2))
            pantalla.blit(texto, texto_rect)
        elif casilla.tipo == "E" and casilla.contenido is not None:
            texto = fuente.render(str(casilla.contenido), True, BLANCO)
            texto_rect = texto.get_rect(center=(columna * self.tamano_celda + self.tamano_celda // 2, fila * self.tamano_celda + self.tamano_celda // 2))
            pantalla.blit(texto, texto_rect)