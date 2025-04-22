import pygame
import csv
import numpy as np

# Inicialización de Pygame
pygame.init()

# Definir dimensiones de la ventana
WIDTH, HEIGHT = 950, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Carro con Péndulo")

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Definir el reloj para controlar la tasa de fotogramas
clock = pygame.time.Clock()

# Cargar datos desde el archivo CSV
def cargar_datos_csv(nombre_archivo):
    time = []
    x_pos = []
    theta = []
    v_carro = []
    fuerza = []
    a_carro = []
    a_pendulo = []
    
    with open(nombre_archivo, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Saltar la cabecera
        for row in reader:
            time.append(float(row[0]))
            x_pos.append(float(row[2]))
            theta.append(float(row[1]))
            v_carro.append(float(row[3]))
            fuerza.append(float(row[4]))
            a_carro.append(float(row[5]))  # Aceleración del carro
            a_pendulo.append(float(row[6]))  # Aceleración del péndulo
    
    return np.array(time), np.array(x_pos), np.array(theta), np.array(v_carro), np.array(fuerza), np.array(a_carro), np.array(a_pendulo)

# Función para dibujar el carro y el péndulo
def dibujar_carro_pendulo(x, theta):
    # Parámetros de la ventana
    carro_width = 60
    carro_height = 40
    pendulum_length = 150  # Longitud del péndulo
    pendulum_radius = 5   # Radio del péndulo (esfera)
    
    # Escalar la posición del carro para que se vea mejor en la ventana
    scaled_x = (x * 50) + WIDTH // 2  # Multiplicamos por 15 para exagerar el movimiento
    
    # Limitar el movimiento del carro para que no se salga de la pantalla
    #scaled_x = max(min(scaled_x, WIDTH - carro_width // 2), carro_width // 2)
    
    # Posición del carro en la pantalla
    carro_y = HEIGHT - 100
    carro_x = WIDTH/2
    
    # Ángulo del péndulo
    pendulum_x = int(scaled_x + pendulum_length * np.sin(np.radians(theta)))
    pendulum_y = int(carro_y - pendulum_length * np.cos(np.radians(theta)))
    
    # Dibujar el carro (rectángulo negro)
    pygame.draw.rect(screen, BLACK, (scaled_x - carro_width // 2, carro_y - carro_height // 2, carro_width, carro_height))
    
    # Dibujar la línea del péndulo
    pygame.draw.line(screen, RED, (scaled_x, carro_y), (pendulum_x, pendulum_y), 5)
    
    # Dibujar el círculo del péndulo (extremo)
    pygame.draw.circle(screen, RED, (pendulum_x, pendulum_y), pendulum_radius)

    # Dibujar el eje X (línea en la parte inferior)
    pygame.draw.line(screen, BLACK, (carro_x - 600, HEIGHT - 50), (carro_x + 600, HEIGHT - 50), 5)  # Línea horizontal

    # Dibujar los indicadores de la posición en el eje X
    for i in range(-20, 21, 5):  # Rango de -20 a 20
        pygame.draw.line(screen, RED, (carro_x + i * 15, HEIGHT - 60), (carro_x + i * 15, HEIGHT - 40), 2)  # Marcadores

# Función principal para la animación
def animar():
    # Cargar los datos desde el CSV
    time, x_pos, theta, v_carro, fuerza, a_carro, a_pendulo = cargar_datos_csv("TP2\\simulacion_resultados.csv")

    # Bucle de la simulación
    running = True
    index = 0
    while running and index < len(time):
        screen.fill(WHITE)  # Limpiar la pantalla

        # Dibujar el carro y el péndulo en la posición actual
        dibujar_carro_pendulo(x_pos[index], theta[index])

        # Mostrar el tiempo, la velocidad del carro, la fuerza, y las aceleraciones
        font = pygame.font.SysFont("Arial", 24)
        time_text = font.render(f"Tiempo: {time[index]:.2f} s", True, BLACK)
        velocity_text = font.render(f"Velocidad Carro: {v_carro[index]:.2f} m/s", True, BLACK)
        force_text = font.render(f"Fuerza: {-fuerza[index]:.2f} N", True, BLACK)
        position_text = font.render(f"Posición: {x_pos[index]:.2f} m*50", True, BLACK)
        a_carro_text = font.render(f"A. Carro: {a_carro[index]:.2f} m/s²", True, BLACK)
        a_pendulo_text = font.render(f"A. Péndulo: {a_pendulo[index]:.2f} rad/s²", True, BLACK)
        
        screen.blit(time_text, (10, 10))
        screen.blit(velocity_text, (10, 40))
        screen.blit(force_text, (10, 70))
        screen.blit(position_text, (WIDTH - 230, 10))  # Mostrar posición en la esquina superior derecha
        screen.blit(a_carro_text, (WIDTH - 230, 40))  # Mostrar aceleración del carro
        screen.blit(a_pendulo_text, (WIDTH - 230, 70))  # Mostrar aceleración del péndulo

        # Actualizar la pantalla
        pygame.display.flip()

        # Control de framerate (ajustado según la aceleración del carro)
        # La aceleración más grande, mayor velocidad en la animación
        max_accel = max(abs(a_carro[index]), abs(a_pendulo[index]))  # Usar la aceleración más grande
        clock.tick(30 + int(max_accel * 100))  # Multiplicar por 5 para exagerar la velocidad de la animación

        # Esperar eventos (como cerrar la ventana)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Incrementar el índice
        index += 1

    # Al finalizar la animación, mantener la ventana abierta unos segundos
    pygame.time.delay(1000)

# Ejecutar la animación
animar()

# Cerrar Pygame
pygame.quit()
