import heapq

class AStar:
    @staticmethod
    def heuristica(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    @staticmethod
    def buscar_camino(tablero, inicio, objetivo):
        abiertos = []
        heapq.heappush(abiertos, (0, inicio))
        padres = {inicio: None}
        costos = {inicio: 0}
        visitados = set()

        while abiertos:
            _, actual = heapq.heappop(abiertos)
            if actual == objetivo:
                camino = []
                while actual:
                    camino.append(actual)
                    actual = padres[actual]
                return camino[::-1]

            visitados.add(actual)

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = actual[0] + dx, actual[1] + dy
                if tablero.transitable(nx, ny) and (nx, ny) not in visitados:
                    nuevo_costo = costos[actual] + 1
                    if (nx, ny) not in costos or nuevo_costo < costos[(nx, ny)]:
                        costos[(nx, ny)] = nuevo_costo
                        prioridad = nuevo_costo + AStar.heuristica((nx, ny), objetivo)
                        heapq.heappush(abiertos, (prioridad, (nx, ny)))
                        padres[(nx, ny)] = actual

        return None