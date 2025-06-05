import numpy as np

class NeuralNetwork:
    def __init__(self):
        self.initialize()

    def initialize(self):
        self.input_size = 6
        self.hidden_size = 10  # Cambiado a 10 neuronas
        self.output_size = 3

        # Inicialización de pesos y bias con tamaño acorde a 10 neuronas ocultas
        self.W1 = np.random.randn(self.hidden_size, self.input_size) * 0.1
        self.B1 = np.zeros((self.hidden_size, 1))

        self.W2 = np.random.randn(self.output_size, self.hidden_size) * 0.1
        self.B2 = np.zeros((self.output_size, 1))

    def think(self, X):
        X = np.array(X).reshape((self.input_size, 1))
        Z1 = np.dot(self.W1, X) + self.B1
        A1 = np.maximum(0, Z1)  # ReLU
        Z2 = np.dot(self.W2, A1) + self.B2
        return self.act(Z2)

    def act(self, output):
        output = output.flatten()
        action = np.argmax(output)

        if action == 0:
            return "JUMP"
        elif action == 1:
            return "DUCK"
        else:
            return "RUN"
