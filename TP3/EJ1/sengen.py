#generar una onda senoidal con numpy y matplotlib
import numpy as np
import matplotlib.pyplot as plt
import time
# Generar datos de una onda senoidal
x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x)
#sumarle a la onda senoidal una coseno con el doble de frecuencia
y += 0.5 * np.cos(2 * x)
# Agregar ruido gaussiano

fig = plt.figure()
#ir agregando plots a la misma figura
plt.plot(x, y, label='Onda Senoidal con Ruido')
newy = np.zeros_like(y)
# Generar 10 ondas senoidales con ruido gaussiano
plt.xlabel('x')
plt.ylabel('y')
plt.title('Onda Senoidal con Ruido Gaussiano')
plt.legend()
plt.grid(True)
plt.show(block=False)

# abrir el archivo sen.txt en modo escritura
with open('sen.txt', 'w') as f:
    for i in range(10):
        # cambiar la semilla del generador de números aleatorios
        np.random.seed(int(time.time() * 1000) % 1000 + i)
        # Generar ruido gaussiano y sumarlo a la onda senoidal
        newy = y+0.4 * np.random.randn(*y.shape)
        plt.plot(x, newy, label=f'Onda Senoidal {i+1}')
        plt.legend()
        plt.pause(0.5)  # Pausa para visualizar cada onda
        plt.draw()  # Actualizar la figura
        # Escribir todos los puntos en el archivo con el formato (x, y)
        for xi, yi in zip(x, newy):
            f.write(f'({xi:.6f}, {yi:.6f})\n')

plt.show()  # Mostrar la figura final


