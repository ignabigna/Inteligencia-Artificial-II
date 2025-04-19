import matplotlib.pyplot as plt

# Clase de funciones de pertenencia
class FuncionPertenencia:
    def __init__(self, tipo, parametros):
        self.tipo = tipo
        self.parametros = parametros
    
    def evaluar(self, x):
        if self.tipo == "triangular":
            a, b, c = self.parametros
            return self._triangular(x, a, b, c)
        elif self.tipo == "trapezoidal":
            a, b, c, d = self.parametros
            return self._trapezoidal(x, a, b, c, d)
        else:
            raise ValueError(f"Tipo de función '{self.tipo}' no reconocido.")
    
    @staticmethod
    def _triangular(x, a, b, c):
        if x <= a or x >= c:
            return 0.0
        elif a < x < b:
            return (x - a) / (b - a)
        elif b < x < c:
            return (c - x) / (c - b)
        elif x == b:
            return 1.0
    
    @staticmethod
    def _trapezoidal(x, a, b, c, d):
        if x <= a or x >= d:
            return 0.0
        elif a < x < b:
            return (x - a) / (b - a)
        elif b <= x <= c:
            return 1.0
        elif c < x < d:
            return (d - x) / (d - c)
        

# Clase para graficar funciones
class GraficadorFunciones:
    def __init__(self, funciones, dominio):
        """
        Constructor para la clase de graficación de funciones de pertenencia.
        
        Parámetros:
            - funciones: Lista de diccionarios que contienen las funciones y sus etiquetas. 
                        Ejemplo: [{"funcion": FuncionPertenencia, "etiqueta": "Temperatura Baja"}, ...]
            - dominio: Lista o array con los valores de x (por ejemplo, np.linspace).
        """
        self.funciones = funciones  # Lista de funciones con etiquetas
        self.dominio = dominio      # Dominio de los valores de entrada
        self.vectores = []          # Lista para almacenar vectores adicionales
    
    def agregarVector(self, vector, etiqueta):
        """
        Agregar un vector al gráfico.
        
        Parámetros:
            - vector: Lista o array de valores (debe coincidir en tamaño con el dominio).
            - etiqueta: Nombre o descripción del vector para la leyenda.
        """
        if len(vector) != len(self.dominio):
            raise ValueError("El vector debe tener el mismo tamaño que el dominio.")
        self.vectores.append({"vector": vector, "etiqueta": etiqueta})
    
    def graficar(self,titulo,etiqueta_dom):
        """
        Grafica todas las funciones de pertenencia superpuestas junto con los vectores agregados.
        """
        plt.figure(figsize=(10, 6))
        
        # Graficar las funciones de pertenencia
        for item in self.funciones:
            funcion = item["funcion"]
            etiqueta = item["etiqueta"]
            valores_y = [funcion.evaluar(x) for x in self.dominio]
            plt.plot(self.dominio, valores_y, label=etiqueta)
        
        # Graficar los vectores adicionales
        for item in self.vectores:
            vector = item["vector"]
            etiqueta = item["etiqueta"]
            plt.plot(self.dominio, vector, linestyle="--", label=etiqueta)  # Graficamos con línea discontinua
        
        # Configuraciones del gráfico
        plt.title(titulo)
        plt.xlabel(etiqueta_dom)
        plt.ylabel("Grado de Pertenencia")
        plt.legend()
        plt.grid()
        plt.show()
    
    def graficarVector(self):
        """
        Grafica únicamente los vectores agregados, sin incluir las funciones de pertenencia.
        """
        if not self.vectores:
            raise ValueError("No se han agregado vectores para graficar.")

        plt.figure(figsize=(10, 6))
        
        # Graficar solamente los vectores
        for item in self.vectores:
            vector = item["vector"]
            etiqueta = item["etiqueta"]
            plt.plot(self.dominio, vector, linestyle="--", label=etiqueta)  # Graficamos con línea discontinua

        # Configuraciones del gráfico
        plt.title("Vectores de Inferencias")
        plt.xlabel("Dominio (x)")
        plt.ylabel("Valor")
        plt.legend()
        plt.grid()
        plt.show()
