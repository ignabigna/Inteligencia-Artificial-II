import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz

# Parámetros del modelo
M = 1.0  # Masa del carro (kg)
m = 0.1  # Masa del péndulo (kg)
l = 0.5  # Longitud del péndulo (m)
g = 9.81  # Gravedad (m/s^2)
dt = 0.01  # Paso de tiempo (s)
sim_time = 10  # Tiempo de simulación (s)

# Condiciones iniciales
theta_0 = np.pi / 4  # Ángulo inicial (rad)
theta_dot_0 = 0  # Velocidad angular inicial (rad/s)
theta = theta_0
theta_dot = theta_dot_0

# Arrays para almacenar los resultados de la simulación
time = np.linspace(0, sim_time, int(sim_time / dt))
theta_vals = []
theta_dot_vals = []

# Función de dinámica del péndulo
def pendulum_dynamics(theta, theta_dot, F):
    denominator = M + m * (1 - np.cos(theta)**2) / (M + m)
    theta_double_dot = (g * np.sin(theta) - np.cos(theta) * (F + m * l * theta_dot**2 * np.sin(theta))) / denominator
    return theta_double_dot

# Función para el controlador difuso
def fuzzy_controller(theta, theta_dot):
    # Definir las funciones de membresía como antes
    x_angle = np.linspace(-30, 30, 300)  # Ángulo: de -30 a 30 grados
    x_velocity = np.linspace(-10, 10, 300)  # Velocidad angular: de -10 a 10 grados/segundo
    x_force = np.linspace(-100, 100, 300)  # Fuerza: de -100 a 100 N
    
    angle_neg = fuzz.trimf(x_angle, [-30, -30, 0])  # Muy Inclinado
    angle_zero = fuzz.trimf(x_angle, [-5, 0, 5])    # Vertical
    angle_pos = fuzz.trimf(x_angle, [0, 30, 30])    # Muy Inclinado

    velocity_neg = fuzz.trimf(x_velocity, [-10, -10, 0])  # Lento
    velocity_zero = fuzz.trimf(x_velocity, [-5, 0, 5])    # Moderado
    velocity_pos = fuzz.trimf(x_velocity, [0, 10, 10])    # Rápido

    # Aplicar reglas de inferencia difusa (esto es solo un ejemplo)
    if theta > 0:
        if theta_dot > 0:
            F = -20  # Fuerza negativa
        else:
            F = 20  # Fuerza positiva
    else:
        if theta_dot > 0:
            F = 20  # Fuerza positiva
        else:
            F = -20  # Fuerza negativa

    return F

# Simulación
for t in time:
    # Controlador difuso para calcular la fuerza
    F = fuzzy_controller(theta, theta_dot)

    # Actualización de la velocidad angular y el ángulo utilizando el método de Euler
    theta_double_dot = pendulum_dynamics(theta, theta_dot, F)
    theta_dot += theta_double_dot * dt
    theta += theta_dot * dt
    
    # Almacenar valores para graficar
    theta_vals.append(theta)
    theta_dot_vals.append(theta_dot)

# Graficar los resultados
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(time, theta_vals, label="Ángulo (θ)")
plt.title("Comportamiento del Péndulo Invertido")
plt.xlabel("Tiempo (s)")
plt.ylabel("Ángulo (rad)")
plt.grid()

plt.subplot(2, 1, 2)
plt.plot(time, theta_dot_vals, label="Velocidad Angular (θ')", color='r')
plt.xlabel("Tiempo (s)")
plt.ylabel("Velocidad Angular (rad/s)")
plt.grid()

plt.tight_layout()
plt.show()
