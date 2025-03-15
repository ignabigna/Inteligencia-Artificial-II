import pygame
from BG_Tablero import Tablero, AStar

# Configurar Pygame
pygame.init()

# Dimensiones del tablero
FILAS, COLUMNAS = 11, 13
TAMANO_CELDA = 50
ANCHO, ALTO = COLUMNAS * TAMANO_CELDA, FILAS * TAMANO_CELDA

# Crear la ventana
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Simulación de Agente con A*")

# Crear el tablero
tablero = Tablero(FILAS, COLUMNAS)

# Posicionar el agente en una casilla recorrible
posicion_inicial = (5, 0)
tablero.posicionAgente("A", *posicion_inicial)

# Elegir una estantería objetivo
estanteria_objetivo = (8, 7)  # Coordenadas de una estantería

# Encontrar la mejor casilla adyacente a la estantería
posicion_destino = None
for dx in [-1, 1]:  # Solo izquierda y derecha
    posible_destino = (estanteria_objetivo[0], estanteria_objetivo[1] + dx)
    if tablero.transitable(*posible_destino):
        posicion_destino = posible_destino
        break

# Si se encontró una posición destino, calcular la ruta con A*
if posicion_destino:
    camino = AStar.buscar_camino(tablero, posicion_inicial, posicion_destino)

# Bucle principal
corriendo = True

while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    # Mover al agente siguiendo el camino calculado
    if camino:
        for paso in camino:
            pygame.time.delay(300)  # Pausa para visualizar el movimiento
            tablero.moverAgente("A", paso[0], paso[1])
            pantalla.fill((0, 0, 0))  # Fondo negro
            tablero.dibujarTablero(pantalla)
            pygame.display.flip()

        camino = None  # Evitar que el agente siga moviéndose después de llegar

pygame.quit()
