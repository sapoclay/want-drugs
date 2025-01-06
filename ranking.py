import os
from config import ranking
import pygame
from config import ANCHO, ALTO

# Funciones para manejo de ranking
def cargar_ranking():
    if os.path.exists("ranking.txt"):
        with open("ranking.txt", "r") as archivo:
            lineas = archivo.readlines()
            return [tuple(linea.strip().split(", ")) for linea in lineas]
    return []

def guardar_ranking(datos_ranking):
    with open("ranking.txt", "w") as archivo:
        for nombre, puntaje in datos_ranking:
            archivo.write(f"{nombre}, {puntaje}\n")
            
# Mostrar ranking
def mostrar_ranking(pantalla):
    # Cargar el ranking actualizado desde el archivo
    datos_ranking = cargar_ranking()

    # Limpiar la pantalla
    pantalla.fill((0, 0, 0))

    # Configurar fuente y texto
    fuente = pygame.font.SysFont(None, 48)
    texto_titulo = fuente.render("Las 5 máximas puntuaciones:", True, (255, 255, 0))
    ancho_texto_titulo = texto_titulo.get_width()
    pantalla.blit(texto_titulo, ((ANCHO - ancho_texto_titulo) // 2, 50))  # Centrando el título

    # Mostrar las primeras 5 entradas del ranking
    for i, (nombre, puntaje) in enumerate(datos_ranking[:5]):
        texto = fuente.render(f"{i + 1}. {nombre}: {puntaje}", True, (255, 255, 255))
        pantalla.blit(texto, (ANCHO // 2 - 200, 150 + i * 40))

    # Si no hay datos en el ranking, mostrar mensaje
    if not datos_ranking:
        texto_vacio = fuente.render("Todavía no hay puntuaciones registradas.", True, (255, 0, 0))
        ancho_texto_vacio = texto_vacio.get_width()
        pantalla.blit(texto_vacio, ((ANCHO - ancho_texto_vacio) // 2, ALTO // 2))

    pygame.display.flip()
    pygame.time.delay(3000)
