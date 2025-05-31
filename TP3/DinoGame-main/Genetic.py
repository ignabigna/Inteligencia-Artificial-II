import random
import numpy as np

def updateNetwork(population):
    # ===================== ESTA FUNCIÓN RECIBE UNA POBLACIÓN A LA QUE SE DEBEN APLICAR MECANISMOS DE SELECCIÓN, =================
    # ===================== CRUCE Y MUTACIÓN. LA ACTUALIZACIÓN DE LA POBLACIÓN SE APLICA EN LA MISMA VARIABLE ====================
    print("=== Actualización de la población ===")
    print("Scores antes:")
    for i, dino in enumerate(population):
        print(f"Individuo {i}: score = {dino.score}")

    selected_indices = select_fittest(population)
    print(f"Seleccionados para reproducción (top 25%): {selected_indices}")

    for i in range(len(population)):
        parent1 = population[random.choice(selected_indices)]
        parent2 = population[random.choice(selected_indices)]
        child_params = evolve(parent1, parent2)

        dino = population[i]
        dino.W1 = child_params['W1']
        dino.B1 = child_params['B1']
        dino.W2 = child_params['W2']
        dino.B2 = child_params['B2']

        dino.score = 0
        dino.alive = True

    print("Scores después (reiniciados a 0 para la nueva generación)")


    #TODA ACCION ACA TIENE QUE AFECTAR A TODA LA LISTA DE POBLACION

    # =============================================================================================================================

def select_fittest(population, retain_fraction=0.30):
    # ===================== FUNCIÓN DE SELECCIÓN =====================
    #Funcion de seleccion con top 25%
    sorted_pop = sorted(enumerate(population), key=lambda x: x[1].score, reverse=True)
    retain_length = max(1, int(len(population) * retain_fraction))  # mínimo 1
    selected_indices = [i for i, dino in sorted_pop[:retain_length]]
    return selected_indices


    # ================================================================

def evolve(parent1, parent2, mutation_rate=0.05, mutation_strength=0.1):
        # ===================== FUNCIÓN DE CRUCE Y MUTACIÓN =====================
    child = {}
    for attr in ['W1', 'B1', 'W2', 'B2']:
        p1_matrix = getattr(parent1, attr)
        p2_matrix = getattr(parent2, attr)

        mask = np.random.rand(*p1_matrix.shape) > 0.5
        child_matrix = np.where(mask, p1_matrix, p2_matrix)

        mutation_mask = np.random.rand(*child_matrix.shape) < mutation_rate
        noise = np.random.randn(*child_matrix.shape) * mutation_strength
        child_matrix = child_matrix + mutation_mask * noise

        child[attr] = child_matrix
    return child


    # ===============================================================
    

     