import pygame
import heapq
import time

# ======= COLORES =======
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# ======= DIMENSIONES =======
rows = 11  # Filas totales
cols = 13  # Columnas totales
tile_size = 40
screen_width = cols * tile_size   # 13 * 40 = 520
screen_height = rows * tile_size  # 11 * 40 = 440

# ======= CONSTRUIMOS EL MAPA (11×13) =======
# Rellenamos con '.' y luego iremos marcando estanterías y carga
mapa = [
    ['.' for _ in range(cols)]
    for _ in range(rows)
]

# 1) Zona de carga 'C' en (3,0)
mapa[3][0] = 'C'

# 2) Marcar con 'X' las 6 estanterías, cada una 4 filas × 2 columnas:
#    - Estanterías superiores: filas 1..4 (4 filas), columnas 2..3, 6..7, 10..11
#    - Estanterías inferiores: filas 6..9, mismas columnas

# Estanterías superiores (fila = 1..4)
for r in range(1, 5):   # 1,2,3,4
    for c in range(2, 4):   # cols 2..3
        mapa[r][c] = 'X'
    for c in range(6, 8):   # cols 6..7
        mapa[r][c] = 'X'
    for c in range(10, 12): # cols 10..11
        mapa[r][c] = 'X'

# Estanterías inferiores (fila = 6..9)
for r in range(6, 10):  # 6,7,8,9
    for c in range(2, 4):
        mapa[r][c] = 'X'
    for c in range(6, 8):
        mapa[r][c] = 'X'
    for c in range(10, 12):
        mapa[r][c] = 'X'

# Fila 0, fila 5 y fila 10 quedan libres

# ======= ASIGNAR PRODUCTOS (1..48) A CADA CELDA 'X' =======
# Ajustamos las funciones para asignar los mismos 6 bloques de 8 productos
# Bloque 1 (filas 1..4, cols 2..3), Bloque 2 (1..4, 6..7), Bloque 3 (1..4, 10..11)
# Bloque 4 (6..9, 2..3), Bloque 5 (6..9, 6..7), Bloque 6 (6..9, 10..11)
estanterias = {}
contador = 1

def asignar_estanteria(f_ini, f_fin, c_ini, c_fin):
    """Asigna secuencialmente productos a las celdas 'X' entre
    filas [f_ini..f_fin), columnas [c_ini..c_fin)."""
    global contador
    for r in range(f_ini, f_fin):
        for c in range(c_ini, c_fin):
            estanterias[str(contador)] = (r, c)
            contador += 1

# Bloques superiores
asignar_estanteria(1, 5, 2, 4)   # Productos 1..8
asignar_estanteria(1, 5, 6, 8)   # 9..16
asignar_estanteria(1, 5, 10, 12) # 17..24

# Bloques inferiores
asignar_estanteria(6, 10, 2, 4)  # 25..32
asignar_estanteria(6, 10, 6, 8)  # 33..40
asignar_estanteria(6, 10, 10, 12)# 41..48

# Invertir para dibujar los números
pos_estanterias = {}
for num, (r, c) in estanterias.items():
    pos_estanterias[(r, c)] = num

# ======= CASILLA ADYACENTE =======
def encontrar_casilla_accesible(ubicacion):
    """Devuelve una casilla '.' adyacente a 'ubicacion'."""
    if not ubicacion:
        return None
    x, y = ubicacion
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols and mapa[nx][ny] == '.':
            return (nx, ny)
    return None

# ======= ENTRADA DE USUARIO =======
# Posición inicial por defecto (0,0)
ingreso_x = input("Fila inicial (Enter=0): ")
ingreso_y = input("Columna inicial (Enter=0): ")
if ingreso_x and ingreso_y:
    inicio = (int(ingreso_x), int(ingreso_y))
else:
    inicio = (5, 0)

num_estanteria = input("N° de estantería (1..48): ")
if num_estanteria in estanterias:
    ub = estanterias[num_estanteria]
    objetivo = encontrar_casilla_accesible(ub)
else:
    objetivo = None

# ======= A* =======
def heuristica(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_estrella(inicio, objetivo):
    if not objetivo:
        return None
    abiertos = []
    heapq.heappush(abiertos, (0, inicio))
    padres = {inicio: None}
    costos = {inicio: 0}
    
    while abiertos:
        _, actual = heapq.heappop(abiertos)
        if actual == objetivo:
            # Reconstruir camino
            camino = []
            while actual:
                camino.append(actual)
                actual = padres[actual]
            return camino[::-1]
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = actual[0] + dx, actual[1] + dy
            if 0 <= nx < rows and 0 <= ny < cols and mapa[nx][ny] in ('.','C'):
                # 'C' también es transitable
                nuevo_costo = costos[actual] + 1
                if (nx, ny) not in costos or nuevo_costo < costos[(nx, ny)]:
                    costos[(nx, ny)] = nuevo_costo
                    prioridad = nuevo_costo + heuristica((nx, ny), objetivo)
                    heapq.heappush(abiertos, (prioridad, (nx, ny)))
                    padres[(nx, ny)] = actual
    return None

# ======= PYGAME =======
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Montacargas con A*")

font = pygame.font.SysFont(None, 20)

def dibujar_mapa():
    screen.fill(WHITE)
    for r in range(rows):
        for c in range(cols):
            cell = mapa[r][c]
            # Fondo blanco si '.' o 'C'
            color = WHITE if cell in ('.','C') else BLACK
            pygame.draw.rect(screen, color, (c*tile_size, r*tile_size, tile_size, tile_size))
            pygame.draw.rect(screen, BLACK, (c*tile_size, r*tile_size, tile_size, tile_size), 1)
            

            
            # Número de la estantería si es 'X'
            if (r, c) in pos_estanterias:
                text_surface = font.render(pos_estanterias[(r,c)], True, (255,255,255))
                rect = text_surface.get_rect(center=(
                    c*tile_size + tile_size/2,
                    r*tile_size + tile_size/2
                ))
                screen.blit(text_surface, rect)

def mover_montacargas(camino):
    for (r, c) in camino:
        dibujar_mapa()
        # Montacargas en azul
        pygame.draw.rect(screen, BLUE, (c*tile_size, r*tile_size, tile_size, tile_size))
        pygame.display.flip()
        time.sleep(0.8)

# Ejecutar A*
camino = a_estrella(inicio, objetivo)
if camino:
    mover_montacargas(camino)
else:
    print("No hay camino disponible.")

# Mantener la ventana
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
