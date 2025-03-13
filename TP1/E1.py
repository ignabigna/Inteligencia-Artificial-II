import pygame
import heapq

# =====================
#    COLORES Y CONST
# =====================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE  = (0, 0, 255)

TILE_SIZE = 40
ROWS = 11
COLS = 13

SCREEN_WIDTH  = COLS * TILE_SIZE  # 13 * 40 = 520
SCREEN_HEIGHT = ROWS * TILE_SIZE  # 11 * 40 = 440

# =========================
#    CLASE: WAREHOUSEMAP
# =========================
class WarehouseMap:
    """
    Se encarga de:
      - Construir el mapa base (arreglo 2D con estanterías, zona de carga, etc.)
      - Almacenar ubicaciones de productos
      - Proveer métodos para saber si una casilla es transitable
    """
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = []
        self.estanterias = {}       # dict:  { '1': (r,c), '2':(r,c), ... }
        self.pos_estanterias = {}   # dict:  { (r,c): '1', (r,c): '2', ... }

        self._crear_mapa()
        self._asignar_estanterias()

    def _crear_mapa(self):
        # Crear mapa lleno de '.'
        self.grid = [['.' for _ in range(self.cols)] for _ in range(self.rows)]
        # Marcar zona de carga 'C' en (5, 0)
        self.grid[5][0] = 'C'
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
        """
        Asigna productos 1..48 a las celdas 'X' en bloques.
        """
        def asignar_bloque(f_ini, f_fin, c_ini, c_fin, contador):
            """
            Asigna secuencialmente productos a las celdas 'X'.
            Retorna el contador actualizado.
            """
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
        Devuelve True si la celda es '.' o 'C'.
        """
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return self.grid[r][c] in ('.', 'C')
        return False

    def dibujar(self, surface, font):
        """
        Dibuja el mapa en la superficie 'surface' de Pygame.
        """
        surface.fill(WHITE)
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                # Fondo blanco si '.' o 'C'; negro si 'X'
                color = WHITE if cell in ('.','C') else BLACK
                pygame.draw.rect(surface, color, (c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE))
                # Borde
                pygame.draw.rect(surface, BLACK, (c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

                # Dibujar el número de la estantería (si existe)
                if (r, c) in self.pos_estanterias:
                    num_est = self.pos_estanterias[(r, c)]
                    text_surf = font.render(num_est, True, (255, 255, 255))
                    rect = text_surf.get_rect(center=(
                        c*TILE_SIZE + TILE_SIZE/2,
                        r*TILE_SIZE + TILE_SIZE/2
                    ))
                    surface.blit(text_surf, rect)

    def encontrar_casilla_accesible(self, ubicacion):
        """
        Devuelve una casilla '.' adyacente a 'ubicacion' (si existe).
        """
        if not ubicacion:
            return None
        x, y = ubicacion
        for dx, dy in [(0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < self.rows and 0 <= ny < self.cols
                    and self.grid[nx][ny] == '.'):
                return (nx, ny)
        return None

# ========================
#     CLASE: ASTAR
# ========================
class AStar:
    """
    Contiene métodos para realizar la búsqueda A* dada una WarehouseMap y posiciones inicio/objetivo.
    """
    @staticmethod
    def heuristica(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    @staticmethod
    def buscar_camino(warehouse_map, inicio, objetivo):
        """
        Retorna la lista de pasos (camino) desde 'inicio' hasta 'objetivo' usando A*.
        """
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

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = actual[0] + dx, actual[1] + dy
                if warehouse_map.es_transitable(nx, ny):
                    nuevo_costo = costos[actual] + 1
                    if (nx, ny) not in costos or nuevo_costo < costos[(nx, ny)]:
                        costos[(nx, ny)] = nuevo_costo
                        prioridad = nuevo_costo + AStar.heuristica((nx, ny), objetivo)
                        heapq.heappush(abiertos, (prioridad, (nx, ny)))
                        padres[(nx, ny)] = actual

        return None

# ========================
#  CLASE: MONTACARGAS
# ========================
class Montacargas:
    """
    Representa al montacargas que recorre el camino.
    - Guarda la posición actual.
    - Guarda la ruta (lista de celdas).
    - Provee método para dibujarse.
    """
    def __init__(self, posicion_inicial):
        self.posicion = posicion_inicial
        self.camino = []
        self.indice_camino = 0

    def asignar_camino(self, camino):
        """Define la ruta a recorrer y reinicia el índice."""
        self.camino = camino if camino else []
        self.indice_camino = 0

    def actualizar(self):
        """Avanza al siguiente paso del camino (si queda)."""
        if self.indice_camino < len(self.camino):
            self.posicion = self.camino[self.indice_camino]
            self.indice_camino += 1

    def dibujar(self, surface):
        """Dibuja el montacargas (un rectángulo azul) en su posición actual."""
        r, c = self.posicion
        pygame.draw.rect(surface, BLUE, (c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE))

# ========================
#   CLASE: ALMACENGAME
# ========================
class AlmacenGame:
    """
    Clase principal que maneja:
      - Inicialización de Pygame.
      - Crea el mapa (WarehouseMap).
      - Crea el montacargas.
      - Calcula el camino con AStar.
      - Bucle principal (eventos, dibujado, lógica).
    """
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Montacargas con A* (OOP)")
        
        self.font = pygame.font.SysFont(None, 20)
        self.clock = pygame.time.Clock()
        
        # Crear el mapa
        self.warehouse_map = WarehouseMap(ROWS, COLS)
        
        # Leer posición inicial y estantería solicitada (simulando lo que antes se hacía con input())
        self.inicio = (5, 0)  # Valor por defecto
        self.estanteria_deseada = "11"  # Por defecto
        
        # Montacargas
        self.montacargas = Montacargas(posicion_inicial=self.inicio)
        
        # Preparar camino
        self._calcular_camino()

    def _calcular_camino(self):
        """
        Usa el AStar para obtener un camino y lo asigna al montacargas.
        """
        if self.estanteria_deseada in self.warehouse_map.estanterias:
            ub = self.warehouse_map.estanterias[self.estanteria_deseada]
            objetivo = self.warehouse_map.encontrar_casilla_accesible(ub)
        else:
            objetivo = None
        
        camino = AStar.buscar_camino(self.warehouse_map, self.inicio, objetivo)
        self.montacargas.asignar_camino(camino)

    def run(self):
        """
        Bucle principal del juego.
        """
        running = True
        while running:
            # Procesar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # Lógica del montacargas: avanzar un paso
            self.montacargas.actualizar()
            
            # Dibujar
            self.warehouse_map.dibujar(self.screen, self.font)
            self.montacargas.dibujar(self.screen)
            
            pygame.display.flip()
            
            # Control de velocidad (~1.25 FPS => 0.8s por frame)
            self.clock.tick(1.25)
        
        pygame.quit()

# ======================
#   EJECUCIÓN DIRECTA
# ======================
if __name__ == "__main__":
    juego = AlmacenGame()
    juego.run()
