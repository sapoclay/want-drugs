import pygame
import sys
import random
from config import *
from ranking import cargar_ranking, guardar_ranking, mostrar_ranking

# Inicializar pygame y configuraciones
def inicializar_pygame():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption('Want drugs?')
    pygame.mixer.init()
    return pantalla


# Funciones para cargar recursos
def cargar_imagen(ruta, tamaño):
    imagen = pygame.image.load(ruta)
    return pygame.transform.scale(imagen, tamaño)

# Función para calcular el nivel
def calcular_nivel(puntaje):
    return puntaje // 20 + 1

# Función para cargar sonidos del juego
def cargar_sonidos():
    pygame.mixer.music.load(RUTAS["musica_fondo"])
    pygame.mixer.music.set_volume(VOLUMEN_INICIAL)
    pygame.mixer.music.play(-1)  # Bucle infinito
    sonido_recoger = pygame.mixer.Sound(RUTAS["sonido_recoger"])
    return sonido_recoger

# Funciones de pausa
def pausar_juego(pantalla):
    fuente = pygame.font.SysFont(None, 72)
    texto = fuente.render("Juego en Pausa", True, (255, 255, 0))
    pantalla.blit(texto, (ANCHO // 2 - 200, ALTO // 2 - 50))
    pygame.display.flip()
    
def mostrar_pantalla_de_carga(pantalla, ruta_imagen):
    pantalla.fill((0, 0, 0))  # Fondo negro

    # Cargar imagen
    imagen_carga = cargar_imagen(ruta_imagen, (300, 300))  # Ajustar tamaño de la imagen
    ancho_imagen, alto_imagen = imagen_carga.get_size()
    pos_x_imagen = (ANCHO - ancho_imagen) // 2
    pos_y_imagen = (ALTO - alto_imagen) // 2 - 50  # Subir un poco para dejar espacio al texto

    # Dibujar imagen
    pantalla.blit(imagen_carga, (pos_x_imagen, pos_y_imagen))

    # Dibujar texto
    fuente = pygame.font.SysFont(None, 48)
    texto = fuente.render("CARGANDO ...", True, (255, 255, 0))
    ancho_texto, alto_texto = texto.get_size()
    pos_x_texto = (ANCHO - ancho_texto) // 2
    pos_y_texto = pos_y_imagen + alto_imagen + 20  # Debajo de la imagen

    pantalla.blit(texto, (pos_x_texto, pos_y_texto))
    pygame.display.flip()
    pygame.time.delay(3000)  # Mostrar durante 3 segundos
    
# Preguntar reinicio
def preguntar_reiniciar(pantalla):
    fuente = pygame.font.SysFont(None, 48)
    while True:
        pantalla.fill((0, 0, 0))
        texto = fuente.render("¿Quieres jugar de nuevo? (S / N)", True, (255, 255, 255))
        ancho_texto_pregunta = texto.get_width()
        pantalla.blit(texto, ((ANCHO - ancho_texto_pregunta) // 2, 50))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_s:
                    return "reiniciar"
                if evento.key == pygame.K_n:
                    return "menu"

# Pantalla de Game Over
def mostrar_game_over(pantalla, puntaje):
    # Detener la música de fondo
    pygame.mixer.music.stop()
    # Sonido de Game Over
    sonido_game_over = pygame.mixer.Sound(RUTAS["game_over"])
    sonido_game_over.play() 
    fuente = pygame.font.SysFont(None, 72)
    texto = fuente.render("Game Over!!", True, (255, 0, 0))
    pantalla.blit(texto, (ANCHO // 2 - 150, ALTO // 2 - 100))
    pygame.display.flip()
    pygame.time.delay(2000)

    nombre = pedir_nombre(pantalla)
    ranking.append((nombre, str(puntaje)))
    ranking.sort(key=lambda x: int(x[1]), reverse=True)
    guardar_ranking(ranking)

    mostrar_ranking(pantalla)
    return preguntar_reiniciar(pantalla)

# Pedir nombre
def pedir_nombre(pantalla):
    fuente = pygame.font.SysFont(None, 48)
    nombre = ""
    while True:
        pantalla.fill((0, 0, 0))
        texto = fuente.render("Introduce tu nombre: " + nombre, True, (255, 255, 255))
        pantalla.blit(texto, (ANCHO // 2 - 300, ALTO // 2 - 50))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nombre:
                    return nombre
                elif evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    if len(nombre) < 10 and evento.unicode.isprintable():
                        nombre += evento.unicode
                        
# Calcular nivel basado en el puntaje
def calcular_nivel(puntaje):
    # Por ejemplo, subir de nivel cada 20 puntos
    return puntaje // 20 + 1

# Mostrar nivel en pantalla
def mostrar_nivel(pantalla, nivel):
    fuente = pygame.font.SysFont(None, 38)
    texto = fuente.render(f"Nivel: {nivel}", True, (0, 0, 0))
    pantalla.blit(texto, (10, 40))

# Mostrar el puntaje
def mostrar_puntaje(pantalla, puntaje):
    fuente = pygame.font.SysFont(None, 38)
    texto = fuente.render(f"Puntos: {puntaje}", True, (0, 0, 0))
    pantalla.blit(texto, (10, 10))