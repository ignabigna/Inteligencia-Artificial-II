import random
import math
import random
import math
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from TP1.Busqueda_Global.BG_AStar import AStar

class TempleSimulado:
<<<<<<<< HEAD:TP1/Genetico/Gen_TempleSimulado.py
    def __init__(self, tablero, orden_pedido, temperatura_inicial=300, temperatura_final=0.2, decaimiento=0.996, max_iteraciones=10000):
========
    def __init__(self, tablero, orden_pedido, temperatura_inicial=300, temperatura_final=0.1, decaimiento=0.998, max_iteraciones=10000):
>>>>>>>> main:TP1/Busqueda_Local/BL_TempleSimulado.py
        self.tablero = tablero
        self.orden_pedido = orden_pedido
        self.temperatura_inicial = temperatura_inicial
        self.temperatura_final = temperatura_final
        self.decaimiento = decaimiento
        self.max_iteraciones = max_iteraciones

    def encontrar_adyacente(self, estanteria_numero):
        for fila in range(self.tablero.filas):
            for columna in range(self.tablero.columnas):
                casilla = self.tablero.grid[fila][columna]
                if casilla.tipo == "E" and casilla.contenido == estanteria_numero:
                    for dx in [-1, 1]:
                        nx, ny = fila, columna + dx
                        if self.tablero.transitable(nx, ny):
                            return (nx, ny)
        return None

    def evaluar_costo(self, orden):
        costo_total = 0
        for i in range(len(orden) - 1):
            estanteria_1 = orden[i]
            estanteria_2 = orden[i + 1]

            adyacente_1 = self.encontrar_adyacente(estanteria_1)
            adyacente_2 = self.encontrar_adyacente(estanteria_2)

            if adyacente_1 and adyacente_2:
                camino = AStar.buscar_camino(self.tablero, adyacente_1, adyacente_2)
                if camino:
                    costo_total += len(camino)
                else:
                    costo_total += float('inf')
            else:
                costo_total += float('inf')
        costo_total += len(AStar.buscar_camino(self.tablero, adyacente_2,(5,0)))
        return costo_total

    def obtener_posicion_estanteria(self, estanteria_numero):
        for fila in range(self.tablero.filas):
            for columna in range(self.tablero.columnas):
                casilla = self.tablero.grid[fila][columna]
                if casilla.tipo == "E" and casilla.contenido == estanteria_numero:
                    return (fila, columna)
        return None

    def obtener_vecino(self, orden):
        nuevo_orden = orden[:]
        i, j = random.sample(range(len(orden)), 2)
        nuevo_orden[i], nuevo_orden[j] = nuevo_orden[j], nuevo_orden[i]
        return nuevo_orden

    def simular(self):
        orden_actual = self.orden_pedido
        costo_actual = self.evaluar_costo(orden_actual)
        mejor_orden = orden_actual
        mejor_costo = costo_actual
        temperatura = self.temperatura_inicial
        iteracion = 0

        while temperatura > self.temperatura_final and iteracion < self.max_iteraciones:
            vecino = self.obtener_vecino(orden_actual)
            costo_vecino = self.evaluar_costo(vecino)

            if costo_vecino < costo_actual or random.random() < math.exp((costo_actual - costo_vecino) / temperatura):
                orden_actual = vecino
                costo_actual = costo_vecino

            if costo_actual < mejor_costo:
                mejor_orden = orden_actual
                mejor_costo = costo_actual

            temperatura *= self.decaimiento
            iteracion += 1

        return mejor_orden,mejor_costo,iteracion,temperatura