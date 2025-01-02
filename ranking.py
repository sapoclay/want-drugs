import os
from config import ranking

# Funciones para manejo de ranking
def cargar_ranking():
    if os.path.exists("ranking.txt"):
        with open("ranking.txt", "r") as archivo:
            lineas = archivo.readlines()
            return [tuple(linea.strip().split(", ")) for linea in lineas]
    return []

def guardar_ranking():
    with open("ranking.txt", "w") as archivo:
        for nombre, puntaje in ranking:
            archivo.write(f"{nombre}, {puntaje}\n")