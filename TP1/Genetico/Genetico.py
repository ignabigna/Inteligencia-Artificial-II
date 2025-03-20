import os
import sys
import csv
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from TP1.Busqueda_Global.BG_Tablero import Tablero
from Gen_TempleSimulado import TempleSimulado

archivo = "TP1/Busqueda_Local/ordenes2.csv"
archivo_poblacion = "poblacion.csv"

ordenes = []

with open(archivo, newline='') as csvfile:
    lector = csv.reader(csvfile)
    for fila in lector:
        ordenes.append([int(producto) for producto in fila])

poblacion = []
# Creacion de la poblacion Inicial
with open(archivo_poblacion, mode='r') as archivo_csv:
    lector = csv.reader(archivo_csv)
    for fila in lector:
        # Convertir cada fila de strings a una lista de enteros
        individuo = list(map(int, fila))
        poblacion.append(individuo)

#defino al tablero
tablero = Tablero(11, 13)

#Funciones de mutacion
def order_crossover_2hijos(padre1, padre2, inicio, fin):
    size = len(padre1)
    
    # Inicializar los hijos como listas vacías
    hijo1 = [None] * size
    hijo2 = [None] * size
    
    # Copiar segmentos del primer y segundo padre
    hijo1[inicio:fin] = padre1[inicio:fin]
    hijo2[inicio:fin] = padre2[inicio:fin]
    
    # Llenar las posiciones restantes en hijo1 con genes de padre2
    pos_hijo1 = fin
    for gene in padre2:
        if gene not in hijo1:
            while hijo1[pos_hijo1 % size] is not None:
                pos_hijo1 += 1
            hijo1[pos_hijo1 % size] = gene
    
    # Llenar las posiciones restantes en hijo2 con genes de padre1
    pos_hijo2 = fin
    for gene in padre1:
        if gene not in hijo2:
            while hijo2[pos_hijo2 % size] is not None:
                pos_hijo2 += 1
            hijo2[pos_hijo2 % size] = gene
    
    return hijo1, hijo2

# Lista para almacenar los hijos
hijos = []

# Realizar cruces para generar 10 hijos
for _ in range(len(poblacion) // 2):
    padre1 = random.choice(poblacion)
    padre2 = random.choice(poblacion)
    
    # Seleccionar puntos de cruce aleatorios
    inicio = random.randint(0, len(padre1) - 2)
    fin = random.randint(inicio + 1, len(padre1))
    
    # Generar dos hijos por cruce
    hijo1, hijo2 = order_crossover_2hijos(padre1, padre2, inicio, fin)
    hijos.append([hijo1,0])
    hijos.append([hijo2,0])

#hijos[Individio_i,num_i
       # I2,num2]

for hijo in hijos:
    ordenesHijo = []

    for orden in ordenes:
        ordenAux = []
        for i in orden:
            ordenAux.append(hijo[0][i])
        ordenesHijo.append(ordenAux)
        #Ordenes hijo, tiene la reorganizacion de todas las ordenes para ese hijo (ese individuo)

    for orden in ordenesHijo:
        _,costo,_,_=TempleSimulado(tablero, orden).simular()

