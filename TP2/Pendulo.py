import numpy as np
import matplotlib.pyplot as plt
from scipy import constants
import csv  # Para guardar el CSV
from FuncionPertenencia import FuncionPertenencia as FP
from FuncionPertenencia import GraficadorFunciones as GF

CONSTANTE_M = 3  # Masa del carro
CONSTANTE_m = 0.5  # Masa del péndulo
CONSTANTE_l = 1  # Longitud del péndulo

### DEFINIR RANGOS ###

# Rango de valores para el ángulo (en radianes)
RangoTG = np.array([15, 20, 90, 90]) * np.pi / 180
RangoTP = np.array([0, 15, 20]) * np.pi / 180
RangoTZ = np.array([-5, 0, 5]) * np.pi / 180

# Rango de valores para la velocidad angular (en radianes/segundo)
RangoOG = np.array([1, 2, 8, 8])
RangoOP = np.array([0, 1, 2])
RangoOZ = np.array([-0.5, 0, 0.5])

# Rango de valores para la fuerza (en Newtons)
RangoFG = np.array([30, 45, 60, 60])
RangoFP = np.array([10, 25, 35])
RangoFZ = np.array([-15, 0, 15])

### FUNCIONES DE PERTENENCIA (no editar) ###

# Funciones de pertenencia para la entrada (Ángulo)
uThetaNG = FP("trapezoidal", [-RangoTG[3], -RangoTG[2], -RangoTG[1], -RangoTG[0]])
uThetaNP = FP("triangular", [-RangoTP[2], -RangoTP[1], -RangoTP[0]])
uThetaZ = FP("triangular", [RangoTZ[0], RangoTZ[1], RangoTZ[2]])
uThetaPP = FP("triangular", [RangoTP[0], RangoTP[1], RangoTP[2]])
uThetaPG = FP("trapezoidal", [RangoTG[0], RangoTG[1], RangoTG[2], RangoTG[3]])

# Funciones de pertenencia para graficar el ángulo en grados
RangoTG_G = RangoTG * 180 / np.pi
RangoTP_G = RangoTP * 180 / np.pi
RangoTZ_G = RangoTZ * 180 / np.pi
uThetaNG_G = FP("trapezoidal", [-RangoTG_G[3], -RangoTG_G[2], -RangoTG_G[1], -RangoTG_G[0]])
uThetaNP_G = FP("triangular", [-RangoTP_G[2], -RangoTP_G[1], -RangoTP_G[0]])
uThetaZ_G = FP("triangular", [RangoTZ_G[0], RangoTZ_G[1], RangoTZ_G[2]])
uThetaPP_G = FP("triangular", [RangoTP_G[0], RangoTP_G[1], RangoTP_G[2]])
uThetaPG_G = FP("trapezoidal", [RangoTG_G[0], RangoTG_G[1], RangoTG_G[2], RangoTG_G[3]])

# Funciones de pertenencia para la entrada (Velocidad Angular)
uOmegaNG = FP("trapezoidal", [-RangoOG[3], -RangoOG[2], -RangoOG[1], -RangoOG[0]])
uOmegaNP = FP("triangular", [-RangoOP[2], -RangoOP[1], -RangoOP[0]])
uOmegaZ = FP("triangular", [RangoOZ[0], RangoOZ[1], RangoOZ[2]])
uOmegaPP = FP("triangular", [RangoOP[0], RangoOP[1], RangoOP[2]])
uOmegaPG = FP("trapezoidal", [RangoOG[0], RangoOG[1], RangoOG[2], RangoOG[3]])

# Funciones de pertenencia para la salida (Fuerza)
uFzaNG = FP("trapezoidal", [-RangoFG[3], -RangoFG[2], -RangoFG[1], -RangoFG[0]])
uFzaNP = FP("triangular", [-RangoFP[2], -RangoFP[1], -RangoFP[0]])
uFzaZ = FP("triangular", [RangoFZ[0], RangoFZ[1], RangoFZ[2]])
uFzaPP = FP("triangular", [RangoFP[0], RangoFP[1], RangoFP[2]])
uFzaPG = FP("trapezoidal", [RangoFG[0], RangoFG[1], RangoFG[2], RangoFG[3]])

### GRAFICAR FUNCIONES DE PERTENENCIA ###

fTheta = [{"funcion": uThetaNG_G, "etiqueta": "Theta_NG"},
            {"funcion": uThetaNP_G, "etiqueta": "Theta_NP"},
            {"funcion": uThetaZ_G, "etiqueta": "Theta_Z"},
            {"funcion": uThetaPP_G, "etiqueta": "Theta_PP"},
            {"funcion": uThetaPG_G, "etiqueta": "Theta_PG"}]
dom_Theta = np.linspace(-RangoTG[3]*180/np.pi, RangoTG[3]*180/np.pi, 1000)

fOmega = [{"funcion": uOmegaNG, "etiqueta": "Omega_NG"},
            {"funcion": uOmegaNP, "etiqueta": "Omega_NP"},
            {"funcion": uOmegaZ, "etiqueta": "Omega_Z"},
            {"funcion": uOmegaPP, "etiqueta": "Omega_PP"},
            {"funcion": uOmegaPG, "etiqueta": "Omega_PG"}]
dom_Omega = np.linspace(-RangoOG[3], RangoOG[3], 1000)

fFuerza = [{"funcion": uFzaNG, "etiqueta": "Fuerza_NG"},
            {"funcion": uFzaNP, "etiqueta": "Fuerza_NP"},
            {"funcion": uFzaZ, "etiqueta": "Fuerza_Z"},
            {"funcion": uFzaPP, "etiqueta": "Fuerza_PP"},
            {"funcion": uFzaPG, "etiqueta": "Fuerza_PG"}]
dom_Fza = np.linspace(-RangoFG[3], RangoFG[3], 1000)


graficoTheta = GF(fTheta, dom_Theta)
graficoOmega = GF(fOmega, dom_Omega)
graficoFuerza = GF(fFuerza, dom_Fza)

### REGLAS DE INFERENCIA ###

def aplicarReglas(theta, omega):
    """
    Aplicar las reglas de inferencia para determinar la potencia de refrigeración
    en base a la temperatura de entrada.
    """
    salidaPG = max(min(uThetaNG.evaluar(theta), uOmegaNG.evaluar(omega)), min(uThetaNP.evaluar(theta), uOmegaNG.evaluar(omega)), min(uThetaNG.evaluar(theta), uOmegaNP.evaluar(omega)), min(uThetaNG.evaluar(theta), uOmegaZ.evaluar(omega)),min(uThetaNP.evaluar(theta),uOmegaNP.evaluar(omega)))
    salidaPP  = max(min(uThetaNP.evaluar(theta), uOmegaZ.evaluar(omega)), min(uThetaZ.evaluar(theta), uOmegaNG.evaluar(omega)), min(uThetaZ.evaluar(theta), uOmegaNP.evaluar(omega)), min(uThetaPP.evaluar(theta), uOmegaNG.evaluar(omega)))
    salidaZ  = max(min(uThetaNG.evaluar(theta), uOmegaPG.evaluar(omega)), min(uThetaNP.evaluar(theta), uOmegaPP.evaluar(omega)), min(uThetaZ.evaluar(theta), uOmegaZ.evaluar(omega)), min(uThetaPP.evaluar(theta), uOmegaNP.evaluar(omega)), min(uThetaPG.evaluar(theta), uOmegaNG.evaluar(omega)),min(uThetaNG.evaluar(theta),uOmegaPP.evaluar(omega)),min(uThetaPG.evaluar(theta),uOmegaNP.evaluar(omega)))
    salidaNP  = max(min(uThetaNP.evaluar(theta), uOmegaPG.evaluar(omega)), min(uThetaZ.evaluar(theta), uOmegaPG.evaluar(omega)), min(uThetaZ.evaluar(theta), uOmegaPP.evaluar(omega)), min(uThetaPP.evaluar(theta), uOmegaZ.evaluar(omega)))
    salidaNG  = max(min(uThetaPG.evaluar(theta), uOmegaPG.evaluar(omega)), min(uThetaPP.evaluar(theta), uOmegaPG.evaluar(omega)), min(uThetaPG.evaluar(theta), uOmegaPP.evaluar(omega)), min(uThetaPG.evaluar(theta), uOmegaZ.evaluar(omega)), min(uThetaPP.evaluar(theta),uOmegaPP.evaluar(omega)))
    return salidaPG, salidaPP, salidaZ, salidaNP, salidaNG


def defuzzificar(salidaPG, salidaPP, salidaZ, salidaNP, salidaNG):
    """
    Realiza la defuzzificación utilizando el método del centroide.
    Combina las salidas difusas activadas en un valor crisp (numérico).
    
    Parámetros:
    - salida_baja, salida_media, salida_alta: grados de activación para cada conjunto de salida.
    
    Retorna:
    - Potencia de enfriamiento como valor crisp.
    """
    # Dominio de la salida (potencia de enfriamiento: 0 a 100)
    x = np.linspace(-RangoFG[3], RangoFG[3], 1000)
    
    # Agregación: combinar las funciones recortadas de salida
    fzaPG = np.array([min(salidaPG, uFzaPG.evaluar(xi)) for xi in x])
    fzaPP = np.array([min(salidaPP, uFzaPP.evaluar(xi)) for xi in x])
    fzaZ = np.array([min(salidaZ, uFzaZ.evaluar(xi)) for xi in x])
    fzaNP = np.array([min(salidaNP, uFzaNP.evaluar(xi)) for xi in x])
    fzaNG = np.array([min(salidaNG, uFzaNG.evaluar(xi)) for xi in x])
    
    # Agregación final (máximo entre las funciones recortadas)
    agregada = np.maximum(fzaPG, np.maximum(fzaPP, np.maximum(fzaZ, np.maximum(fzaNP, fzaNG))))

    # Defuzzificación: cálculo del centroide
    numerador = np.sum(agregada * x)
    denominador = np.sum(agregada)
    
    if denominador == 0:  # Evitar división entre cero
        print("Error: denominador es cero. No se puede calcular el centroide.")
        return 0
    
    return numerador / denominador  #, agregada

# Calcula la aceleración en el siguiente instante de tiempo dado el ángulo, la velocidad angular actual, y la fuerza ejercida
def calcula_aceleracion(theta, v, f):
    numerador = constants.g * np.sin(theta) + np.cos(theta) * ((-f - CONSTANTE_m * CONSTANTE_l * np.power(v, 2) * np.sin(theta)) / (CONSTANTE_M + CONSTANTE_m))
    denominador = CONSTANTE_l * (4 / 3 - (CONSTANTE_m * np.power(np.cos(theta), 2) / (CONSTANTE_M + CONSTANTE_m)))
    return numerador / denominador

def simular_con_posicion(t_max, delta_t, theta_0, v_0, a_0, x_0, v_carro_0):
    theta = (theta_0 * np.pi) / 180  # Ángulo en radianes
    v = v_0  # Velocidad angular
    a = a_0  # Aceleración angular
    x = x_0  # Posición del carro
    v_carro = v_carro_0  # Velocidad del carro

    # Variables para almacenar los resultados
    y_theta = []  # Para almacenar el ángulo
    y_x = []  # Para almacenar la posición del carro
    y_v_carro = []  # Para almacenar la velocidad del carro
    y_fuerza = []  # Para almacenar la fuerza

    # Crear el tiempo de simulación
    t = np.arange(0, t_max, delta_t)
    
    for ti in t:
        salidaPG, salidaPP, salidaZ, salidaNP, salidaNG = aplicarReglas(theta, v)
        fuerza_crisp = defuzzificar(salidaPG, salidaPP, salidaZ, salidaNP, salidaNG)

        # Calcular la aceleración angular del péndulo
        a = calcula_aceleracion(theta, v, -fuerza_crisp)
        
        # Actualizar la posición del carro y su velocidad
        a_carro = (fuerza_crisp - CONSTANTE_m * CONSTANTE_l * (v**2 * np.sin(theta))) / (CONSTANTE_M + CONSTANTE_m)
        v_carro += a_carro * delta_t  # Velocidad del carro
        x += v_carro * delta_t  # Actualizar la posición del carro

        # Actualizar el ángulo y la velocidad angular
        v += a * delta_t  # Velocidad angular
        theta += v * delta_t + a * np.power(delta_t, 2) / 2  # Actualización del ángulo

        # Almacenar los resultados
        y_theta.append(theta * 180 / np.pi)  # Convertir el ángulo de vuelta a grados
        y_x.append(-x)  # Almacenar la posición del carro
        y_v_carro.append(-v_carro)  # Almacenar la velocidad del carro
        y_fuerza.append(fuerza_crisp)  # Almacenar la fuerza aplicada

        # Verificar si el péndulo se ha caído
        if abs(theta * 180 / np.pi) >= 90:
            print("El péndulo ha caído")
            break

    # Guardar los resultados en un archivo CSV
    with open('simulacion_resultados.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Tiempo (s)", "Ángulo (grados)", "Posición del Carro (m)", "Velocidad del Carro (m/s)", "Fuerza (N)"])
        for i in range(len(t)):
            writer.writerow([t[i], y_theta[i], y_x[i], y_v_carro[i], y_fuerza[i]])

    # Gráfico del ángulo y la posición del carro en la misma ventana pero en gráficos separados
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))  # Crear dos subgráficos

    # Gráfico del ángulo
    ax1.plot(t, y_theta, color='tab:blue')
    ax1.set_xlabel('Tiempo (s)')
    ax1.set_ylabel('Ángulo (grados)', color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax1.set_title('Ángulo vs Tiempo')
    ax1.grid(True)

    # Gráfico de la posición del carro
    ax2.plot(t, y_x, color='tab:red')
    ax2.set_xlabel('Tiempo (s)')
    ax2.set_ylabel('Posición del Carro (m)', color='tab:red')
    ax2.tick_params(axis='y', labelcolor='tab:red')
    ax2.set_title('Posición del Carro vs Tiempo')
    ax2.grid(True)

    # Mostrar los dos gráficos
    plt.tight_layout()  # Ajusta los subgráficos para que no se solapen
    plt.show()

    # Gráfico de la velocidad del carro, la velocidad angular y la fuerza
    fig, ax3 = plt.subplots(figsize=(10, 6))

    # Gráfico de la velocidad del carro
    ax3.plot(t, y_v_carro, color='tab:green')
    ax3.set_xlabel('Tiempo (s)')
    ax3.set_ylabel('Velocidad del Carro (m/s)', color='tab:green')
    ax3.tick_params(axis='y', labelcolor='tab:green')

    # Crear un segundo eje Y para la velocidad angular y la fuerza
    ax4 = ax3.twinx()

    # Gráfico de la velocidad angular

    # Gráfico de la fuerza
    ax4.plot(t, y_fuerza, color='tab:orange', label='Fuerza (N)')
    ax4.set_ylabel('Fuerza (N)', color='tab:orange')
    ax4.tick_params(axis='y', labelcolor='tab:orange')

    # Título y leyenda
    ax3.set_title('Velocidad del Carro, Velocidad Angular y Fuerza vs Tiempo')
    ax3.grid(True)
    ax4.legend(loc='upper right')

    # Mostrar el gráfico de la velocidad y la fuerza
    plt.tight_layout()
    plt.show()


# Simulación con posición y velocidad del carro
simular_con_posicion(5, 0.001, -20, 3, 0, 0, 0)
#tiempo, deltaT, angulo inicial, velocidad angular, posicion del carro, velocidad del carro