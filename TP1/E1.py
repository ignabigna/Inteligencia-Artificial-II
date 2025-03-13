import pygame
import heapq

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
mapa = [
    ['.' for _ in range(cols)]
    for _ in range(rows)
]

# 1) Zona de carga 'C' en (3,0)
mapa[3][0] = 'C'

# 2) Marcar con 'X' las 6 estanterías, cada una 4 filas × 2 columnas:
#    - Estanterías superiores: filas 1..4 (4 filas), columnas 2..3, 6..7, 10..11
#    - Estanterías inferiores: filas 6..9, mismas columnas
for r in range(1, 5):   # filas 1..4 (superiores)
    for c in range(2, 4):   # columnas 2..3
        mapa[r][c] = 'X'
    for c in range(6, 8):   # columnas 6..7
        mapa[r][c] = 'X'
    for c in range(10, 12): # columnas 10..11
        mapa[r][c] = 'X'

for r in range(6, 10):  # filas 6..9 (inferiores)
    for c in range(2, 4):
        mapa[r][c] = 'X'
    for c in range(6, 8):
        mapa[r][c] = 'X'
    for c in range(10, 12):
        mapa[r][c] = 'X'

# ======= ASIGNAR PRODUCTOS (1..48) A CADA CELDA 'X' =======
estanterias = {}
contador = 1

def asignar_estanteria(f_ini, f_fin, c_ini, c_fin):
    global contador
    for rr in range(f_ini, f_fin):
        for cc in range(c_ini, c_fin):
            estanterias[str(contador)] = (rr, cc)
            contador += 1

# Bloques superiores
asignar_estanteria(1, 5, 2, 4)    #  1.. 8
asignar_estanteria(1, 5, 6, 8)    #  9..16
asignar_estanteria(1, 5, 10, 12)  # 17..24

# Bloques inferiores
asignar_estanteria(6, 10, 2, 4)   # 25..32
asignar_estanteria(6, 10, 6, 8)   # 33..40
asignar_estanteria(6, 10, 10, 12) # 41..48

# Diccionario inverso para dibujar números en pantalla
pos_estanterias = {}
for num, (r, c) in estanterias.items():
    pos_estanterias[(r, c)] = num

# ======= CASILLA ADYACENTE =======
def encontrar_casilla_accesible(ubicacion):
    """Devuelve una casilla '.' adyacente a 'ubicacion' (si existe)."""
    if not ubicacion:
        return None
    x, y = ubicacion
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols and mapa[nx][ny] == '.':
            return (nx, ny)
    return None

# ======= ENTRADA DE USUARIO =======
# Posición inicial por defecto (5,0) en lugar de (0,0)
ingreso_x = input("Fila inicial (Enter=5): ")
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
    """Retorna la lista de pasos (camino) desde 'inicio' hasta 'objetivo'."""
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
            # '.' y 'C' son transitables
            if 0 <= nx < rows and 0 <= ny < cols and mapa[nx][ny] in ('.', 'C'):
                nuevo_costo = costos[actual] + 1
                if (nx, ny) not in costos or nuevo_costo < costos[(nx, ny)]:
                    costos[(nx, ny)] = nuevo_costo
                    prioridad = nuevo_costo + heuristica((nx, ny), objetivo)
                    heapq.heappush(abiertos, (prioridad, (nx, ny)))
                    padres[(nx, ny)] = actual
    return None

# Calculamos el camino
camino = a_estrella(inicio, objetivo)

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
            # Fondo blanco si '.' o 'C', negro si 'X'
            color = WHITE if cell in ('.','C') else BLACK
            pygame.draw.rect(screen, color, (c*tile_size, r*tile_size, tile_size, tile_size))
            # Borde de la celda
            pygame.draw.rect(screen, BLACK, (c*tile_size, r*tile_size, tile_size, tile_size), 1)

            # Dibujar número en celdas de estantería
            if (r, c) in pos_estanterias:
                text_surface = font.render(pos_estanterias[(r,c)], True, (255, 255, 255))
                rect = text_surface.get_rect(center=(
                    c*tile_size + tile_size/2,
                    r*tile_size + tile_size/2
                ))
                screen.blit(text_surface, rect)

# --- BUCLE PRINCIPAL DE JUEGO ---
clock = pygame.time.Clock()
running = True
indice_camino = 0

while running:
    # Procesa eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Dibuja el mapa
    dibujar_mapa()

    # Si hay camino y aún no llegamos al final
    if camino and indice_camino < len(camino):
        r, c = camino[indice_camino]
        pygame.draw.rect(screen, BLUE, (c*tile_size, r*tile_size, tile_size, tile_size))
        indice_camino += 1
    else:
        # Si ya finalizó el camino, dibujamos la última posición (si existe)
        if camino:
            r, c = camino[-1]
            pygame.draw.rect(screen, BLUE, (c*tile_size, r*tile_size, tile_size, tile_size))

    pygame.display.flip()

    # Controla la velocidad (aprox. 1.25 FPS => ~0.8s por “frame”)
    clock.tick(1.25)

pygame.quit()
