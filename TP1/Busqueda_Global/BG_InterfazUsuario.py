from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QInputDialog
from PyQt6.QtCore import pyqtSignal
import sys
import pygame
import threading
from BG_Tablero import Tablero, AStar

class InterfazUsuario(QWidget):
    llegada_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()
        self.tablero = Tablero(11, 13)
        self.agente_pos = None
        self.llegada_signal.connect(self.mensaje_llegada)

    def initUI(self):
        self.setWindowTitle("Menu de Recoleccion de Paquetes")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.label_pregunta = QLabel("¿Dónde quiere iniciar el agente?")
        layout.addWidget(self.label_pregunta)

        self.boton_carga = QPushButton("Zona de carga")
        self.boton_carga.clicked.connect(lambda: self.iniciar_agente("C"))
        layout.addWidget(self.boton_carga)

        self.boton_manual = QPushButton("Seleccionar otra casilla")
        self.boton_manual.clicked.connect(self.pedir_coordenadas)
        layout.addWidget(self.boton_manual)

        self.label_estanteria = QLabel("Ingrese número de estantería a visitar:")
        layout.addWidget(self.label_estanteria)
        self.input_estanteria = QLineEdit()
        layout.addWidget(self.input_estanteria)

        self.boton_iniciar = QPushButton("Iniciar recorrido")
        self.boton_iniciar.clicked.connect(self.iniciar_recorrido)
        layout.addWidget(self.boton_iniciar)

        self.boton_reiniciar = QPushButton("Reiniciar")
        self.boton_reiniciar.clicked.connect(self.reiniciar_simulacion)
        layout.addWidget(self.boton_reiniciar)

        self.setLayout(layout)

    def iniciar_agente(self, opcion):
        if opcion == "C":
            self.agente_pos = (5, 0)
            self.tablero.posicionAgente("A", 5, 0)
        self.mostrar_mensaje("El agente ha sido colocado en la zona de carga. Ahora seleccione una estantería.")

    def pedir_coordenadas(self):
        coordenadas, ok = QInputDialog.getText(self, "Ingresar coordenadas", "Ingrese fila y columna separadas por una coma:")
        if ok and coordenadas:
            try:
                fila, columna = map(int, coordenadas.split(","))

                if self.tablero.grid[fila][columna].tipo == "E":
                    self.mostrar_mensaje("No puede colocar el agente en una estantería. Elija otra casilla.")
                    return

                if self.tablero.transitable(fila, columna):
                    self.agente_pos = (fila, columna)
                    self.tablero.posicionAgente("A", fila, columna)
                    self.mostrar_mensaje(f"El agente ha sido colocado en ({fila}, {columna}). Ahora seleccione una estantería.")
                else:
                    self.mostrar_mensaje("Casilla no válida. Debe ser una casilla recorrible.")

            except ValueError:
                self.mostrar_mensaje("Entrada inválida. Ingrese números separados por una coma.")

    def iniciar_recorrido(self):
        if not self.agente_pos:
            self.mostrar_mensaje("Debe colocar al agente primero.")
            return

        self.tablero.reiniciarTablero()

        numero_estanteria = self.input_estanteria.text()
        if not numero_estanteria.isdigit():
            self.mostrar_mensaje("Ingrese un número de estantería válido.")
            return

        numero_estanteria = int(numero_estanteria)
        estanteria_objetivo = None

        for fila in range(self.tablero.filas):
            for columna in range(self.tablero.columnas):
                casilla = self.tablero.grid[fila][columna]
                if casilla.tipo == "E" and casilla.contenido == numero_estanteria:
                    estanteria_objetivo = (fila, columna)
                    break

        if not estanteria_objetivo:
            self.mostrar_mensaje("No se encontró la estantería con ese número.")
            return

        destino = self.tablero.encontrarEstanteria(*estanteria_objetivo)
        if not destino:
            self.mostrar_mensaje("No hay una casilla recorrible junto a la estantería.")
            return
        
        if self.agente_pos == destino:
            self.mostrar_mensaje("Ya se encuentra en esta estantería. Seleccione otra diferente.")
            return

        camino = AStar.buscar_camino(self.tablero, self.agente_pos, destino)
        if not camino:
            self.mostrar_mensaje("No se encontró un camino hacia la estantería.")
            return

        threading.Thread(target=self.simular_movimiento, args=(camino,), daemon=True).start()

    def simular_movimiento(self, camino):
        pygame.init()
        pantalla = pygame.display.set_mode((650, 550))
        pygame.display.set_caption("Movimiento del Agente")
        reloj = pygame.time.Clock()
        corriendo = True

        while corriendo:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    corriendo = False
                    pygame.quit()
                    return

            if camino:
                paso = camino.pop(0)
                self.tablero.moverAgente("A", paso[0], paso[1])
                self.agente_pos = (paso[0], paso[1])
                pantalla.fill((0, 0, 0))
                self.tablero.dibujarTablero(pantalla)
                pygame.display.flip()
                pygame.time.delay(300)
                reloj.tick(30)
            else:
                corriendo = False
                pygame.quit()
                self.llegada_signal.emit()

    def mensaje_llegada(self):
        self.mostrar_mensaje("El agente ha llegado a la estantería. Puede seleccionar otra estantería a visitar.")

    def reiniciar_simulacion(self):
        self.agente_pos = None
        self.tablero = Tablero(11, 13)
        self.mostrar_mensaje("Simulación reiniciada. Seleccione el inicio del agente.")

    def mostrar_mensaje(self, mensaje):
        QMessageBox.information(self, "Información", mensaje)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = InterfazUsuario()
    ventana.show()
    sys.exit(app.exec())