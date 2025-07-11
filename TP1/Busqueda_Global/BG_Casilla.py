class Casilla:
    def __init__(self, tipo="R", contenido=None):
        self.tipo = tipo
        self.contenido = contenido
        self.visita = False
        self.ocupacion = None
        self.color = (255, 255, 255)

    def registrar_visita(self):
        if self.tipo == "E":
            self.visita = True

    def ocupar(self, agente):
        if self.ocupacion is None:
            self.ocupacion = agente
            return True
        return False

    def liberar(self):
        self.ocupacion = None