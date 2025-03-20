from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QInputDialog
from PyQt6.QtCore import pyqtSignal, QTimer
import sys
import pygame
import threading
from BG_Tablero import Tablero
from BG_AStar import AStar

class InterfazUsuario(QWidget):
    llegada_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.tablero = Tablero(11, 13)
        self.tamano_celda = self.tablero.tamano_celda
        self.agente_pos = None
        self.estanterias_visitadas = set()
        self.llegada_signal.connect(self.mostrar_mensaje_llegada)

    def init_ui(self):
        self.setWindowTitle("Menú de Recolección de Paquetes")
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
            self.tablero.posicion_agente("A", 5, 0)
        self.mostrar_mensaje("El agente ha sido colocado en la zona de carga. Ahora seleccione una estantería.")

    def pedir_coordenadas(self):
        coordenadas, ok = QInputDialog.getText(self, "Ingresar coordenadas", "Ingrese fila y columna separadas por una coma:")
        if ok and coordenadas:
            try:
                fila, columna = map(int, coordenadas.split(","))
                if self.tablero.transitable(fila, columna):
                    self.agente_pos = (fila, columna)
                    self.tablero.posicion_agente("A", fila, columna)
                    self.mostrar_mensaje(f"El agente ha sido colocado en ({fila}, {columna}). Ahora seleccione una estantería.")
                else:
                    self.mostrar_mensaje("Casilla no válida. Debe ser una casilla recorrible.")
            except ValueError:
                self.mostrar_mensaje("Entrada inválida. Ingrese números separados por una coma.")

    def iniciar_recorrido(self):
        if not self.agente_pos:
            self.mostrar_mensaje("Debe colocar al agente primero.")
            return

        self.tablero.reiniciar_tablero()

        numero_estanteria = self.input_estanteria.text()
        if not numero_estanteria.isdigit():
            self.mostrar_mensaje("Ingrese un número de estantería válido.")
            return

        numero_estanteria = int(numero_estanteria)
        if numero_estanteria in self.estanterias_visitadas:
            self.mostrar_mensaje("Esta estantería ya ha sido visitada. Seleccione otra.")
            return

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

        destino = self.tablero.encontrar_estanteria(*estanteria_objetivo)
        if not destino:
            self.mostrar_mensaje("No hay una casilla recorrible junto a la estantería.")
            return

        camino = AStar.buscar_camino(self.tablero, self.agente_pos, destino)
        if not camino:
            self.mostrar_mensaje("No se encontró un camino hacia la estantería.")
            return

        self.estanterias_visitadas.add(numero_estanteria)
        threading.Thread(target=self.simular_movimiento, args=(camino,), daemon=True).start()

    def simular_movimiento(self, camino):
        pygame.quit()
        pygame.init()
        pantalla = pygame.display.set_mode((910, 770))
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
                self.tablero.mover_agente("A", paso[0], paso[1])
                self.agente_pos = (paso[0], paso[1])

                if self.tablero.grid[paso[0]][paso[1]].tipo != "C":
                    self.tablero.colorear_casilla(paso[0], paso[1], (128, 191, 255))

                pantalla.fill((0, 0, 0))
                self.tablero.dibujar_tablero(pantalla)
                pygame.display.flip()
                pygame.time.delay(300)
                reloj.tick(30)
            else:
                corriendo = False
                pygame.quit()
                self.tablero.limpiar_tablero()
                self.llegada_signal.emit()

    def mostrar_mensaje_llegada(self):
        self.mostrar_mensaje("El agente ha llegado a la estantería. Puede seleccionar otra estantería a visitar.")

    def reiniciar_simulacion(self):
        self.agente_pos = None
        self.estanterias_visitadas.clear()
        self.tablero = Tablero(11, 13)
        self.mostrar_mensaje("Simulación reiniciada. Seleccione el inicio del agente.")

    def mostrar_mensaje(self, mensaje):
        mensaje_box = QMessageBox(self)
        mensaje_box.setText(mensaje)
        mensaje_box.setWindowTitle("Información")
        mensaje_box.setStandardButtons(QMessageBox.StandardButton.Ok)

        def cerrar_mensaje():
            mensaje_box.close()

        QTimer.singleShot(2000, cerrar_mensaje)
        mensaje_box.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = InterfazUsuario()
    ventana.show()
    sys.exit(app.exec())