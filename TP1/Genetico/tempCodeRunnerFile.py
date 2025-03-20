import random
def mutar(poblacion):
    for individuo in poblacion:
        if random.random() < 0.2:
            cantidad_mutaciones = random.randint(1, 10)
            for _ in range(cantidad_mutaciones):
                idx1 = random.randint(0, len(individuo[0]) - 1)
                idx2 = random.randint(0, len(individuo[0]) - 1)
                individuo[0][idx1], individuo[0][idx2] = individuo[0][idx2], individuo[0][idx1]
    return poblacion

print(mutar([[[1,2,3,4,5,6,7,8,9,10],0]]))