import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

X = []
y = []

with open('sen.txt', 'r') as f:
    for line in f:
        line = line.strip().replace('(', '').replace(')', '')
        if line:
            x_val, y_val = line.split(',')
            X.append(float(x_val))
            y.append(float(y_val))

X = np.array(X).reshape(-1, 1)
y = np.array(y)

# Modelo MLP
model = Sequential([
    Dense(12, activation='relu', input_shape=(1,)),
    Dense(12, activation='relu'),
    Dense(1)
])

model.compile(optimizer='adam', loss='mse')
history = model.fit(X, y, epochs=200, verbose=0)

X_fit = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
y_fit = model.predict(X_fit)


plt.scatter(X, y, label='Datos originales')
plt.plot(X_fit, y_fit, color='red', label='Modelo MLP')
plt.legend()
plt.xlabel('X')
plt.ylabel('y')
plt.title('Regresión con red neuronal multicapa')
plt.show()
