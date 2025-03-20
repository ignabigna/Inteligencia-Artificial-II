from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QInputDialog
from PyQt6.QtCore import pyqtSignal, QTimer
import sys
import pygame
import threading
import csv
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from TP1.Busqueda_Global.BG_Tablero import Tablero
from TP1.Busqueda_Global.BG_AStar import AStar
from BL_TempleSimulado import TempleSimulado

class InterfazUsuario(QWidget):
    llegada_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()
        self.tablero = Tablero(11, 13)
        self.tamano_celda = self.tablero.tamano_celda
        self.agente_pos = None
        self.ordenes = self.cargarOrdenes("TP1/Busqueda_Local/ordenes.csv")
        self.orden_actual = 0
        self.llegada_signal.connect(self.mensajeLlegada)
        self.estanterias_visitadas = set()

    def initUI(self):
        self.setWindowTitle("Simulación de Recolector de Paquetes")
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

        self.label_estanteria = QLabel("Inicie el recorrido o finalice el programa")
        layout.addWidget(self.label_estanteria)

        self.boton_iniciar = QPushButton("Iniciar recorrido")
        self.boton_iniciar.clicked.connect(self.iniciarRecorrido)
        layout.addWidget(self.boton_iniciar)

        self.boton_reiniciar = QPushButton("Cerrar programa")
        self.boton_reiniciar.clicked.connect(self.cerrarPrograma)
        layout.addWidget(self.boton_reiniciar)

        self.orden_label = QLabel("Orden de recolección: ")
        layout.addWidget(self.orden_label)

        self.setLayout(layout)

    def cargarOrdenes(self, archivo):
        ordenes = []
        with open(archivo, newline='') as csvfile:
            lector = csv.reader(csvfile)
            for fila in lector:
                ordenes.append([int(producto) for producto in fila])
        return ordenes

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

    def calcularOrdenOptimo(self, sa):
        orden_optimo = sa.simular()

        self.orden_label.setText(f"Orden de recolección: {'-> '.join(map(str, orden_optimo))}")

        self.hilo_simulacion = threading.Thread(target=self.simularRecorrido, args=(orden_optimo,))
        self.hilo_simulacion.start()

    def iniciarRecorrido(self):
        if not self.agente_pos:
            self.mostrarMensaje("Debe colocar al agente primero.")
            return

        self.tablero.reiniciarTablero()
        orden_pedido = self.ordenes[self.orden_actual]
        sa = TempleSimulado(self.tablero, orden_pedido)
        threading.Thread(target=self.calcularOrdenOptimo, args=(sa,)).start()
    
    def movimientoPorCamino(self, camino, pantalla):
        for paso in camino:
            fila, columna = paso
            self.tablero.moverAgente("A", fila, columna)
            self.agente_pos = (fila, columna)

            if self.tablero.grid[fila][columna].tipo != "C":
                self.tablero.colorearCasilla(fila, columna, (128, 191, 255))

            pantalla.fill((0, 0, 0))
            self.tablero.dibujarTablero(pantalla)
            pygame.display.flip()
            pygame.time.delay(300)

        self.llegada_signal.emit()

    def simularRecorrido(self, orden_optimo):
        pygame.quit()
        pygame.init()

        pantalla = pygame.display.set_mode((900, 770))
        pygame.display.set_caption("Simulación de Recolector")

        for estanteria in orden_optimo:
            estanteria_objetivo = None
            for fila in range(self.tablero.filas):
                for columna in range(self.tablero.columnas):
                    casilla = self.tablero.grid[fila][columna]
                    if casilla.tipo == "E" and casilla.contenido == estanteria:
                        estanteria_objetivo = (fila, columna)
                        break

            if estanteria_objetivo:
                destino = self.tablero.encontrarEstanteria(*estanteria_objetivo)
                if destino:
                    camino = AStar.buscar_camino(self.tablero, self.agente_pos, destino)
                    if camino:
                        self.movimientoPorCamino(camino, pantalla)
                    else:
                        self.mostrarMensaje(f"No se encontró un camino hacia la estantería {estanteria}.")
                        break
                else:
                    self.mostrarMensaje(f"No se encontró la estantería {estanteria}.")
                    break

            pygame.time.delay(500)

        self.tablero.limpiarTablero()
        self.mostrarBotones()

    def simularMovimiento(self, camino, pantalla):
        for paso in camino:
            self.tablero.moverAgente("A", paso[0], paso[1])
            self.agente_pos = (paso[0], paso[1])

            if self.tablero.grid[paso[0]][paso[1]].tipo != "C":
                self.tablero.colorearCasilla(paso[0], paso[1], (128, 191, 255))

            pantalla.fill((0, 0, 0))
            self.tablero.dibujarTablero(pantalla)
            pygame.display.flip()
            pygame.time.delay(300)

        self.llegada_signal.emit()

    def mostrarBotones(self):
        self.boton_iniciar.setEnabled(True)
        self.boton_iniciar.setText("Iniciar siguiente pedido")
        self.boton_iniciar.clicked.disconnect()
        self.boton_iniciar.clicked.connect(self.siguientePedido)

    def siguientePedido(self):
        self.orden_actual += 1
        if self.orden_actual < len(self.ordenes):
            self.iniciarRecorrido()
        else:
            self.mostrarMensaje("Todos los pedidos han sido procesados.")
            self.boton_iniciar.setEnabled(False)

    def reiniciarSimulacion(self):
        self.agente_pos = None
        self.estanterias_visitadas.clear()
        self.tablero = Tablero(11, 13)
        self.mostrarMensaje("Simulación reiniciada. Seleccione el inicio del agente.")

    def mostrarMensaje(self, mensaje):
        mensaje_box = QMessageBox(self)
        mensaje_box.setText(mensaje)
        mensaje_box.setWindowTitle("Información")
        mensaje_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        
        def cerrar_mensaje():
            mensaje_box.close()

        QTimer.singleShot(2000, cerrar_mensaje)
        mensaje_box.exec()

    def mensajeLlegada(self):
        self.mostrarMensaje("El agente ha llegado a la estantería.")

    def cerrarPrograma(self):
        QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = InterfazUsuario()
    ventana.show()
    sys.exit(app.exec())