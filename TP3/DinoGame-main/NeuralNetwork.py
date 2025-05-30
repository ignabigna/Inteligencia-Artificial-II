import numpy as np

class NeuralNetwork:
    def __init__(self):
        self.initialize()

    def initialize(self):
        # Tamaños de la red: 5 entradas, 1 capa oculta con 6 neuronas, 3 salidas (JUMP, DUCK, RUN)
        self.input_size = 5
        self.hidden_size = 6
        self.output_size = 3

        # Inicialización de pesos con valores pequeños aleatorios
        self.W1 = np.random.randn(self.hidden_size, self.input_size) * 0.1
        self.B1 = np.zeros((self.hidden_size, 1))

        self.W2 = np.random.randn(self.output_size, self.hidden_size) * 0.1
        self.B2 = np.zeros((self.output_size, 1))

        # ============================================================================================

    def think(self, X):
        # Aseguramos que X sea un vector columna
        X = np.array(X).reshape((self.input_size, 1))

        # Primera capa: W1 * X + B1 → ReLU
        Z1 = np.dot(self.W1, X) + self.B1
        A1 = np.maximum(0, Z1)  # Función de activación ReLU

        # Segunda capa: W2 * A1 + B2 → salida
        Z2 = np.dot(self.W2, A1) + self.B2

        return self.act(Z2)

        # ========================================================================================
        #return self.act(result)

    def act(self, output):
        # ======================== USE THE ACTIVATION FUNCTION TO ACT =============================
        output = output.flatten()         # Convierte (3x1) → (3,)
        action = np.argmax(output)        # Selecciona la acción con mayor valor

        if action == 0:
            return "JUMP"
        elif action == 1:
            return "DUCK"
        else:
            return "RUN"