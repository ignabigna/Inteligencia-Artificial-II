###################################
# warehouse_map.py
###################################
import random
import pygame

class WarehouseMap:
    """
    Representa el mapa:
      - grid: matriz con '.', 'C', 'X'
      - estanterias: {str(numero): (r, c)}
      - pos_estanterias: {(r, c): str(numero)}
    """

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = []
        self.estanterias = {}
        self.pos_estanterias = {}
        self._crear_mapa()
        self._asignar_estanterias()

        # Aquí guardamos las celdas 'pintadas' (visitadas) por cada montacargas
        # como sets de tuplas (r, c).
        # Ej: self.trayectoria_mc1 = set(), self.trayectoria_mc2 = set()
        self.trayectoria_mc1 = set()
        self.trayectoria_mc2 = set()

    def _crear_mapa(self):
        # Crear mapa lleno de '.'
        self.grid = [['.' for _ in range(self.cols)] for _ in range(self.rows)]
        # Marcar zona de carga 'C' en (3, 0)
        self.grid[3][0] = 'C'

        # Añadir bloques de estanterías 'X'
        # Estanterías superiores (filas 1..4)
        for r in range(1, 5):
            for c in range(2, 4):
                self.grid[r][c] = 'X'
            for c in range(6, 8):
                self.grid[r][c] = 'X'
            for c in range(10, 12):
                self.grid[r][c] = 'X'

        # Estanterías inferiores (filas 6..9)
        for r in range(6, 10):
            for c in range(2, 4):
                self.grid[r][c] = 'X'
            for c in range(6, 8):
                self.grid[r][c] = 'X'
            for c in range(10, 12):
                self.grid[r][c] = 'X'

    def _asignar_estanterias(self):
        def asignar_bloque(f_ini, f_fin, c_ini, c_fin, contador):
            for rr in range(f_ini, f_fin):
                for cc in range(c_ini, c_fin):
                    self.estanterias[str(contador)] = (rr, cc)
                    self.pos_estanterias[(rr, cc)] = str(contador)
                    contador += 1
            return contador

        contador = 1
        # Bloques superiores
        contador = asignar_bloque(1, 5, 2, 4, contador)    # 1..8
        contador = asignar_bloque(1, 5, 6, 8, contador)    # 9..16
        contador = asignar_bloque(1, 5, 10, 12, contador)  # 17..24
        # Bloques inferiores
        contador = asignar_bloque(6, 10, 2, 4, contador)   # 25..32
        contador = asignar_bloque(6, 10, 6, 8, contador)   # 33..40
        contador = asignar_bloque(6, 10, 10, 12, contador) # 41..48

    def es_transitable(self, r, c):
        """
        Retorna True si la celda está dentro de límites y si es '.' o 'C'.
        """
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return self.grid[r][c] in ('.', 'C')
        return False

    def encontrar_casilla_accesible(self, ubicacion):
        """
        Devuelve una celda '.' adyacente a 'ubicacion' (si existe), o None.
        """
        if not ubicacion:
            return None
        x, y = ubicacion
        for dx, dy in [(0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.rows and 0 <= ny < self.cols:
                if self.grid[nx][ny] == '.':
                    return (nx, ny)
        return None

    def dibujar(self, surface, font, tile_size, colors):
        """
        Dibuja el mapa y las trayectorias en la pantalla.
        - Pintamos las celdas por donde pasó cada montacargas con otro color.
        """
        WHITE = colors['WHITE']
        BLACK = colors['BLACK']
        SURFACE_MC1 = colors['TRAIL_MC1']  # Color para la trayectoria de MC1
        SURFACE_MC2 = colors['TRAIL_MC2']  # Color para la trayectoria de MC2

        surface.fill(WHITE)
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]

                # Determinar color de fondo base
                if cell in ('.', 'C'):
                    color_fondo = WHITE
                else:
                    color_fondo = BLACK

                # Si esta celda pertenece al camino que recorrió MC1...
                if (r, c) in self.trayectoria_mc1:
                    color_fondo = SURFACE_MC1

                # Si también la recorrió MC2, podrías mezclar colores
                # Pero en este ejemplo, la sobre-escribimos con MC2
                if (r, c) in self.trayectoria_mc2:
                    color_fondo = SURFACE_MC2

                pygame.draw.rect(surface, color_fondo,
                                 (c*tile_size, r*tile_size, tile_size, tile_size))
                # Borde de la celda
                pygame.draw.rect(surface, BLACK,
                                 (c*tile_size, r*tile_size, tile_size, tile_size), 1)

                # Dibujar número de estantería si está en pos_estanterias
                if (r, c) in self.pos_estanterias:
                    num_est = self.pos_estanterias[(r, c)]
                    text_surf = font.render(num_est, True, (255,255,255))
                    rect = text_surf.get_rect(center=(
                        c*tile_size + tile_size/2,
                        r*tile_size + tile_size/2
                    ))
                    surface.blit(text_surf, rect)

###################################
# astar.py
###################################
import heapq

class AStar:
    """
    Clase utilitaria para buscar caminos con A*.
    """

    @staticmethod
    def heuristica(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    @staticmethod
    def buscar_camino(warehouse_map, inicio, objetivo, obstaculos_adicionales=None):
        """
        Retorna la lista de pasos (camino) desde 'inicio' hasta 'objetivo'.
        'obstaculos_adicionales' es un set de celdas (r, c) que se considerarán
        no transitables durante la búsqueda (por ej. la posición de otro montacargas).
        """
        if not objetivo:
            return None

        if obstaculos_adicionales is None:
            obstaculos_adicionales = set()

        abiertos = []
        heapq.heappush(abiertos, (0, inicio))
        padres = {inicio: None}
        costos = {inicio: 0}

        while abiertos:
            _, actual = heapq.heappop(abiertos)
            if actual == objetivo:
                # Reconstruir camino
                camino = []
                while actual is not None:
                    camino.append(actual)
                    actual = padres[actual]
                return camino[::-1]

            # Explorar vecinos
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = actual[0] + dx, actual[1] + dy

                # Verificar si es transitable y no está en obstaculos_adicionales
                if warehouse_map.es_transitable(nx, ny) and (nx, ny) not in obstaculos_adicionales:
                    nuevo_costo = costos[actual] + 1
                    if (nx, ny) not in costos or nuevo_costo < costos[(nx, ny)]:
                        costos[(nx, ny)] = nuevo_costo
                        prioridad = nuevo_costo + AStar.heuristica((nx, ny), objetivo)
                        heapq.heappush(abiertos, (prioridad, (nx, ny)))
                        padres[(nx, ny)] = actual

        return None

###################################
# montacargas.py
###################################
class Montacargas:
    """
    Clase que representa un montacargas:
      - Guarda posición actual.
      - Guarda el camino (lista de celdas).
      - Avanza paso a paso.
    """

    def __init__(self, id_mc, posicion_inicial, color=None):
        """
        id_mc: identificador (1 o 2).
        posicion_inicial: tupla (r, c).
        color: color de pygame para dibujar (opcional, lo manejaremos desde fuera).
        """
        self.id_mc = id_mc
        self.posicion = posicion_inicial
        self.camino = []
        self.indice_camino = 0
        self.color = color  # Podríamos no usarlo si lo dibujamos desde fuera

    def asignar_camino(self, camino):
        """Define la ruta a recorrer y reinicia el índice."""
        self.camino = camino if camino else []
        self.indice_camino = 0

    def actualizar(self):
        """Avanza un paso en el camino (si hay pasos restantes)."""
        if self.indice_camino < len(self.camino):
            self.posicion = self.camino[self.indice_camino]
            self.indice_camino += 1

    def llego_destino(self):
        """Indica si el montacargas ya completó su recorrido."""
        return self.indice_camino >= len(self.camino)

###################################
# almacen_game.py
###################################
import pygame

import random

class AlmacenGame:
    def __init__(self):
        # Parámetros
        self.ROWS = 11
        self.COLS = 13
        self.TILE_SIZE = 40

        self.SCREEN_WIDTH  = self.COLS * self.TILE_SIZE
        self.SCREEN_HEIGHT = self.ROWS * self.TILE_SIZE

        # Colores
        self.colors = {
            'WHITE': (255,255,255),
            'BLACK': (0,0,0),
            'BLUE':  (0,0,255),
            'RED':   (255,0,0),
            # Colores de las trayectorias
            'TRAIL_MC1': (180, 180, 255),  # un celeste claro
            'TRAIL_MC2': (255, 200, 200)   # un rosado claro
        }

        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Dos Montacargas con A* y Evitación de Colisión")

        self.font = pygame.font.SysFont(None, 20)
        self.clock = pygame.time.Clock()

        # Crear el mapa
        self.warehouse_map = WarehouseMap(self.ROWS, self.COLS)

        # Montacargas 1: inicio fijo, estantería fija
        self.mc1 = Montacargas(id_mc=1, posicion_inicial=(5,0))

        # Montacargas 2: inicio aleatorio
        r_random = random.randint(0, self.ROWS-1)
        c_random = random.randint(0, self.COLS-1)
        # Asegurarnos de que sea transitable
        while not self.warehouse_map.es_transitable(r_random, c_random):
            r_random = random.randint(0, self.ROWS-1)
            c_random = random.randint(0, self.COLS-1)
        self.mc2 = Montacargas(id_mc=2, posicion_inicial=(r_random, c_random))

        # Elegir estantería al azar para MC2
        lista_estanterias = list(self.warehouse_map.estanterias.keys())
        estanteria_azar = random.choice(lista_estanterias)

        # Definir los objetivos
        self.estanteria_deseada_mc1 = "48"  # fijo
        self.estanteria_deseada_mc2 = "15"

        # Calcular los caminos iniciales
        self._calcular_camino_inicial(self.mc1, self.estanteria_deseada_mc1)
        self._calcular_camino_inicial(self.mc2, self.estanteria_deseada_mc2)

    def _calcular_camino_inicial(self, montacargas, num_estanteria):
        """Calcula el camino de un montacargas a una estantería dada."""
        if num_estanteria in self.warehouse_map.estanterias:
            ub = self.warehouse_map.estanterias[num_estanteria]
            objetivo = self.warehouse_map.encontrar_casilla_accesible(ub)
        else:
            objetivo = None

        # No tenemos obstaculos_adicionales en el cálculo inicial
        camino = AStar.buscar_camino(self.warehouse_map,
                                     montacargas.posicion,
                                     objetivo)
        montacargas.asignar_camino(camino)

    def run(self):
        running = True
        while running:
            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Lógica Montacargas 2: 
            #   - MC2 simplemente avanza por su ruta.
            #   - Si llega a destino, ya no se mueve más (en este ejemplo).
            if not self.mc2.llego_destino():
                self.mc2.actualizar()
                # Marcar trayectoria MC2
                self.warehouse_map.trayectoria_mc2.add(self.mc2.posicion)

            # Lógica Montacargas 1:
            #   - Antes de moverse, verificamos si su próximo paso está "bloqueado" por MC2.
            #   - Si el siguiente paso es la posición de MC2, recalculamos la ruta (A*) 
            #     considerando la posición actual de MC2 como obstáculo.
            if not self.mc1.llego_destino():
                # Revisar el siguiente paso de la ruta
                prox_idx = self.mc1.indice_camino
                if prox_idx < len(self.mc1.camino):
                    siguiente_celda = self.mc1.camino[prox_idx]
                    # Si esa celda coincide con la posición de MC2 => recalcular
                    if siguiente_celda == self.mc2.posicion:
                        self._recalcular_ruta_mc1()
                
                # Ahora sí, avanzar
                self.mc1.actualizar()
                # Marcar trayectoria MC1
                self.warehouse_map.trayectoria_mc1.add(self.mc1.posicion)

            # Dibujar
            self.warehouse_map.dibujar(self.screen, self.font,
                                       self.TILE_SIZE, self.colors)
            # Dibujar montacargas
            self._dibujar_montacargas(self.mc1, self.colors['BLUE'])
            self._dibujar_montacargas(self.mc2, self.colors['RED'])

            pygame.display.flip()
            self.clock.tick(2)  # 2 FPS => 0.5s por frame

        pygame.quit()

    def _recalcular_ruta_mc1(self):
        """
        Recalcula la ruta de Montacargas 1 al objetivo,
        tomando la posición de MC2 como obstáculo adicional.
        """
        # Saber a qué estantería iba MC1
        num_estanteria = self.estanteria_deseada_mc1
        if num_estanteria in self.warehouse_map.estanterias:
            ub = self.warehouse_map.estanterias[num_estanteria]
            objetivo = self.warehouse_map.encontrar_casilla_accesible(ub)
        else:
            objetivo = None

        # Ahora definimos un set de "obstáculos" que incluya la posición de MC2
        obstaculos_extra = { self.mc2.posicion }
        
        camino = AStar.buscar_camino(
            self.warehouse_map,
            self.mc1.posicion,
            objetivo,
            obstaculos_adicionales=obstaculos_extra
        )
        self.mc1.asignar_camino(camino)

    def _dibujar_montacargas(self, montacargas, color):
        r, c = montacargas.posicion
        pygame.draw.rect(
            self.screen,
            color,
            (c*self.TILE_SIZE, r*self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
        )

###################################
# main.py
###################################
def main():
    juego = AlmacenGame()
    juego.run()

if __name__ == "__main__":
    main()
