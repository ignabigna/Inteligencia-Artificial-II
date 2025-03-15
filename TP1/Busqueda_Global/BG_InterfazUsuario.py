from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QInputDialog
from PyQt6.QtCore import pyqtSignal
import sys
import pygame
import threading
from BG_Tablero import Tablero, AStar

AGENTE_IMG_PATH = "TP1/Imagenes/Rick.png"

class InterfazUsuario(QWidget):
    llegada_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()
        self.tablero = Tablero(11, 13)
        self.tamano_celda = self.tablero.tamano_celda
        self.agente_pos = None
        self.llegada_signal.connect(self.mensajeLlegada)
        self.imagen_agente = pygame.image.load(AGENTE_IMG_PATH)
        self.imagen_agente = pygame.transform.scale(self.imagen_agente, (self.tamano_celda, self.tamano_celda))
        self.estanterias_visitadas = set()

    def initUI(self):
        self.setWindowTitle("Menu de Recoleccion de Paquetes")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.label_pregunta = QLabel("¿Dónde quiere iniciar el agente?")
        layout.addWidget(self.label_pregunta)

        self.boton_carga = QPushButton("Zona de carga")
        self.boton_carga.clicked.connect(lambda: self.iniciarAgente("C"))
        layout.addWidget(self.boton_carga)

        self.boton_manual = QPushButton("Seleccionar otra casilla")
        self.boton_manual.clicked.connect(self.pedirCoordenadas)
        layout.addWidget(self.boton_manual)

        self.label_estanteria = QLabel("Ingrese número de estantería a visitar:")
        layout.addWidget(self.label_estanteria)
        self.input_estanteria = QLineEdit()
        layout.addWidget(self.input_estanteria)

        self.boton_iniciar = QPushButton("Iniciar recorrido")
        self.boton_iniciar.clicked.connect(self.iniciarRecorrido)
        layout.addWidget(self.boton_iniciar)

        self.boton_reiniciar = QPushButton("Reiniciar")
        self.boton_reiniciar.clicked.connect(self.reiniciarSimulacion)
        layout.addWidget(self.boton_reiniciar)

        self.setLayout(layout)

    def iniciarAgente(self, opcion):
        if opcion == "C":
            self.agente_pos = (5, 0)
            self.tablero.posicionAgente("A", 5, 0)
        self.mostrarMensaje("El agente ha sido colocado en la zona de carga. Ahora seleccione una estantería.")

    def pedirCoordenadas(self):
        coordenadas, ok = QInputDialog.getText(self, "Ingresar coordenadas", "Ingrese fila y columna separadas por una coma:")
        if ok and coordenadas:
            try:
                fila, columna = map(int, coordenadas.split(","))
                if self.tablero.transitable(fila, columna):
                    self.agente_pos = (fila, columna)
                    self.tablero.posicionAgente("A", fila, columna)
                    self.mostrarMensaje(f"El agente ha sido colocado en ({fila}, {columna}). Ahora seleccione una estantería.")
                else:
                    self.mostrarMensaje("Casilla no válida. Debe ser una casilla recorrible.")
            except ValueError:
                self.mostrarMensaje("Entrada inválida. Ingrese números separados por una coma.")

    def iniciarRecorrido(self):
        if not self.agente_pos:
            self.mostrarMensaje("Debe colocar al agente primero.")
            return

        self.tablero.reiniciarTablero()

        numero_estanteria = self.input_estanteria.text()
        if not numero_estanteria.isdigit():
            self.mostrarMensaje("Ingrese un número de estantería válido.")
            return

        numero_estanteria = int(numero_estanteria)
        if numero_estanteria in self.estanterias_visitadas:
            self.mostrarMensaje("Esta estantería ya ha sido visitada. Seleccione otra.")
            return

        estanteria_objetivo = None
        for fila in range(self.tablero.filas):
            for columna in range(self.tablero.columnas):
                casilla = self.tablero.grid[fila][columna]
                if casilla.tipo == "E" and casilla.contenido == numero_estanteria:
                    estanteria_objetivo = (fila, columna)
                    break

        if not estanteria_objetivo:
            self.mostrarMensaje("No se encontró la estantería con ese número.")
            return

        destino = self.tablero.encontrarEstanteria(*estanteria_objetivo)
        if not destino:
            self.mostrarMensaje("No hay una casilla recorrible junto a la estantería.")
            return

        camino = AStar.buscar_camino(self.tablero, self.agente_pos, destino)
        if not camino:
            self.mostrarMensaje("No se encontró un camino hacia la estantería.")
            return

        self.estanterias_visitadas.add(numero_estanteria)
        threading.Thread(target=self.simularMovimiento, args=(camino,), daemon=True).start()

    def simularMovimiento(self, camino):
        pygame.quit()
        pygame.init()
        pantalla = pygame.display.set_mode((900, 750))
        pygame.display.set_caption("Movimiento del Recolector")
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
                pantalla.blit(self.imagen_agente, (self.agente_pos[1] * self.tamano_celda, self.agente_pos[0] * self.tamano_celda))
                pygame.display.flip()
                pygame.time.delay(300)
                reloj.tick(30)
            else:
                corriendo = False
                pygame.quit()
                self.llegada_signal.emit()

    def mensajeLlegada(self):
        self.mostrarMensaje("El agente ha llegado a la estantería. Puede seleccionar otra estantería a visitar.")

    def reiniciarSimulacion(self):
        self.agente_pos = None
        self.estanterias_visitadas.clear()
        self.tablero = Tablero(11, 13)
        self.mostrarMensaje("Simulación reiniciada. Seleccione el inicio del agente.")

    def mostrarMensaje(self, mensaje):
        QMessageBox.information(self, "Información", mensaje)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = InterfazUsuario()
    ventana.show()
    sys.exit(app.exec())