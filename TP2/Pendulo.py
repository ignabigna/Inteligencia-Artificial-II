#Funcionando para pequeños ángulos
import numpy as np
import matplotlib.pyplot as plt
from scipy import constants
from FuncionPertenencia import FuncionPertenencia as FP
from FuncionPertenencia import GraficadorFunciones as GF


CONSTANTE_M = 2 # Masa del carro
CONSTANTE_m = 1 # Masa de la pertiga
CONSTANTE_l = 1 # Longitud dela pertiga


#EDITAR RANGOS

#Rangos mejorados
RangoTG = np.array([15, 20, 90, 90])*np.pi/180
RangoTP = np.array([0, 15, 20])*np.pi/180
RangoTZ = np.array([-5, 0, 5])*np.pi/180


RangoOG = np.array([1,2,8,8])
RangoOP = np.array([0,1,2])
RangoOZ = np.array([-0.5,0,0.5])

RangoFG = np.array([30,45,60,60])
RangoFP = np.array([10,25,35])
RangoFZ = np.array([-15,0,15])


"""
RangoOG = np.array([0.26,0.35,3,3])
RangoOP = np.array([0,0.17,0.35])
RangoOZ = np.array([-0.04,0,0.04])  #aprox 2°/s
"""

### FUNCIONES DE PERTENENCIA (no editar) ###

#funciones de pertenencia para la entrada1 (Ángulo)
uThetaNG = FP("trapezoidal", [-RangoTG[3],-RangoTG[2],-RangoTG[1],-RangoTG[0]])
uThetaNP = FP("triangular", [-RangoTP[2],-RangoTP[1],-RangoTP[0]])
uThetaZ = FP("triangular", [RangoTZ[0],RangoTZ[1],RangoTZ[2]])
uThetaPP = FP("triangular", [RangoTP[0],RangoTP[1],RangoTP[2]])
uThetaPG = FP("trapezoidal", [RangoTG[0],RangoTG[1],RangoTG[2],RangoTG[3]])

#funciones de pertenencia para graficar el angulo en grados
RangoTG_G = RangoTG*180/np.pi
RangoTP_G = RangoTP*180/np.pi
RangoTZ_G = RangoTZ*180/np.pi
uThetaNG_G = FP("trapezoidal", [-RangoTG_G[3],-RangoTG_G[2],-RangoTG_G[1],-RangoTG_G[0]])
uThetaNP_G = FP("triangular", [-RangoTP_G[2],-RangoTP_G[1],-RangoTP_G[0]])
uThetaZ_G = FP("triangular", [RangoTZ_G[0],RangoTZ_G[1],RangoTZ_G[2]])
uThetaPP_G = FP("triangular", [RangoTP_G[0],RangoTP_G[1],RangoTP_G[2]])
uThetaPG_G = FP("trapezoidal", [RangoTG_G[0],RangoTG_G[1],RangoTG_G[2],RangoTG_G[3]])

#funciones de pertenencia para la entrada2 (Velocidad Angular)
uOmegaNG = FP("trapezoidal", [-RangoOG[3],-RangoOG[2],-RangoOG[1],-RangoOG[0]])
uOmegaNP = FP("triangular", [-RangoOP[2],-RangoOP[1],-RangoOP[0]])
uOmegaZ = FP("triangular", [RangoOZ[0],RangoOZ[1],RangoOZ[2]])
uOmegaPP = FP("triangular", [RangoOP[0],RangoOP[1],RangoOP[2]])
uOmegaPG = FP("trapezoidal", [RangoOG[0],RangoOG[1],RangoOG[2],RangoOG[3]])

#funciones de pertenencia para la salida (Fuerza)
uFzaNG = FP("trapezoidal", [-RangoFG[3],-RangoFG[2],-RangoFG[1],-RangoFG[0]])
uFzaNP = FP("triangular", [-RangoFP[2],-RangoFP[1],-RangoFP[0]])
uFzaZ = FP("triangular", [RangoFZ[0],RangoFZ[1],RangoFZ[2]])
uFzaPP = FP("triangular", [RangoFP[0],RangoFP[1],RangoFP[2]])
uFzaPG = FP("trapezoidal", [RangoFG[0],RangoFG[1],RangoFG[2],RangoFG[3]])

### GRAFICAR FUNCIONES DE PERTENENCIA ###

fTheta =    [{"funcion": uThetaNG_G, "etiqueta": "Theta_NG"},
            {"funcion": uThetaNP_G, "etiqueta": "Theta_NP"},
            {"funcion": uThetaZ_G, "etiqueta": "Theta_Z"},
            {"funcion": uThetaPP_G, "etiqueta": "Theta_PP"},
            {"funcion": uThetaPG_G, "etiqueta": "Theta_PG"}]
dom_Theta = np.linspace(-RangoTG[3]*180/np.pi, RangoTG[3]*180/np.pi, 1000)

fOmega =    [{"funcion": uOmegaNG, "etiqueta": "Omega_NG"},
            {"funcion": uOmegaNP, "etiqueta": "Omega_NP"},
            {"funcion": uOmegaZ, "etiqueta": "Omega_Z"},
            {"funcion": uOmegaPP, "etiqueta": "Omega_PP"},
            {"funcion": uOmegaPG, "etiqueta": "Omega_PG"}]
dom_Omega = np.linspace(-RangoOG[3], RangoOG[3], 1000)

fFuerza =   [{"funcion": uFzaNG, "etiqueta": "Fuerza_NG"},
            {"funcion": uFzaNP, "etiqueta": "Fuerza_NP"},
            {"funcion": uFzaZ, "etiqueta": "Fuerza_Z"},
            {"funcion": uFzaPP, "etiqueta": "Fuerza_PP"},
            {"funcion": uFzaPG, "etiqueta": "Fuerza_PG"}]
dom_Fza = np.linspace(-RangoFG[3], RangoFG[3], 1000)


graficoTheta = GF(fTheta, dom_Theta)
graficoOmega = GF(fOmega, dom_Omega)
graficoFuerza = GF(fFuerza, dom_Fza)

# Activar el que se desee graficar

#graficoTheta.graficar("Funciones de pertenencia para el ángulo (Theta)", "Ángulo")
#graficoOmega.graficar("Funciones de pertenencia para la velocidad angular (Omega)", "Velocidad Angular")
#graficoFuerza.graficar("Funciones de pertenencia para la fuerza", "Fuerza")

### REGLAS DE INFERENCIA ###

def aplicarReglas(theta, omega):
    """
    Aplicar las reglas de inferencia para determinar la potencia de refrigeración
    en base a la temperatura de entrada.
    """
    # Aplicar las reglas de inferencia
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
    """
    acá se recortan las funciones de pertenencia de salida según los grados de activación
    por ejemplo el vector pot baja se llena posición a posición siempre que uPotBaja(xi) sea menor que la salida_baja (constante)
    cuando llegue a ser igual o mayor, el vector pot_baja se sigue llenando hasta tener el mismo tamaño que x
    pero con el valor constante de salida_baja que funciona como un techo
    """
    fzaPG = np.array([min(salidaPG, uFzaPG.evaluar(xi)) for xi in x])
    fzaPP = np.array([min(salidaPP, uFzaPP.evaluar(xi)) for xi in x])
    fzaZ = np.array([min(salidaZ, uFzaZ.evaluar(xi)) for xi in x])
    fzaNP = np.array([min(salidaNP, uFzaNP.evaluar(xi)) for xi in x])
    fzaNG = np.array([min(salidaNG, uFzaNG.evaluar(xi)) for xi in x])
    
    # Agregación final (máximo entre las funciones recortadas)
    """
    acá se hace la agregación final, se toma el máximo entre las funciones recortadas.
    el vector agrgada contiene, en cada una de sus posiciones (igual al vector x) el valor mas grande
    entre las posiciones de pot_baja, pot_media y pot_alta
    """
    agregada = np.maximum(fzaPG, np.maximum(fzaPP, np.maximum(fzaZ, np.maximum(fzaNP, fzaNG))))

    # Defuzzificación: cálculo del centroide
    numerador = np.sum(agregada * x)
    denominador = np.sum(agregada)
    
    if denominador == 0:  # Evitar división entre cero
        print("Error: denominador es cero. No se puede calcular el centroide.")
        return 0
    
    return numerador / denominador  #, agregada

def simular(t_max, delta_t, theta_0, v_0, a_0):
    theta = (theta_0 * np.pi) / 180
    v = v_0
    a = a_0

    # Simular
    y = []

    x = np.arange(0, t_max, delta_t)
    for t in x:
        salidaPG, salidaPP, salidaZ, salidaNP, salidaNG = aplicarReglas(theta, v)
        fuerza_crisp = defuzzificar(salidaPG, salidaPP, salidaZ, salidaNP, salidaNG)

        print("velocidad:", v, "theta:", theta*180/np.pi, "fuerza crisp", fuerza_crisp)
        a = calcula_aceleracion(theta, v, -fuerza_crisp)
        v = v + a * delta_t
        theta = theta + v * delta_t + a * np.power(delta_t, 2) / 2
        y.append(theta*180/np.pi)
        if abs(theta*180/np.pi) >= 90:
            print("se cayó")
            break

    fig, ax = plt.subplots()
    ax.plot(x, y)

    ax.set(xlabel='time (s)', ylabel='theta', title='Delta t = ' + str(delta_t) + " s")
    ax.grid()

    plt.show()


# Calcula la aceleracion en el siguiente instante de tiempo dado el angulo y la velocidad angular actual, y la fuerza ejercida
def calcula_aceleracion(theta, v, f):
    numerador = constants.g * np.sin(theta) + np.cos(theta) * ((-f - CONSTANTE_m * CONSTANTE_l * np.power(v, 2) * np.sin(theta)) / (CONSTANTE_M + CONSTANTE_m))
    denominador = CONSTANTE_l * (4/3 - (CONSTANTE_m * np.power(np.cos(theta), 2) / (CONSTANTE_M + CONSTANTE_m)))
    return numerador / denominador

simular(4, 0.001, -35, 0, 0)

