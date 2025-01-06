import pygame
import random
import sys
import os
from config import *
from menu import mostrar_menu_inicial   
from ranking import cargar_ranking, guardar_ranking, mostrar_ranking
from utils import (
    inicializar_pygame,
    cargar_imagen,
    cargar_sonidos,
    pausar_juego,
    mostrar_pantalla_de_carga,
    preguntar_reiniciar,
    mostrar_game_over,
    calcular_nivel,
    mostrar_nivel,
    mostrar_puntaje,
)

# Funciones para manejar eventos
def manejar_eventos():
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

# Funciones de control de volumen
def manejar_volumen(teclas):
    global muteado
    if teclas[pygame.K_m]:  # Alternar mute
        muteado = not muteado
        if muteado:
            pygame.mixer.music.set_volume(0.0)
        else:
            pygame.mixer.music.set_volume(0.5)  # Volumen predeterminado al desmutear

    if not muteado:  # Solo ajustar volumen si no está muteado
        if teclas[pygame.K_PLUS] or teclas[pygame.K_KP_PLUS]:
            volumen_actual = pygame.mixer.music.get_volume()
            pygame.mixer.music.set_volume(min(1.0, volumen_actual + 0.1))
        if teclas[pygame.K_MINUS] or teclas[pygame.K_KP_MINUS]:
            volumen_actual = pygame.mixer.music.get_volume()
            pygame.mixer.music.set_volume(max(0.0, volumen_actual - 0.1))
            
# Mover al jugador
def mover_jugador(teclas, jugador_x):
    # Reducir el valor 15 hará que el jugador se mueva más lentamente, aumentando la dificultad.
    if teclas[pygame.K_LEFT] and jugador_x > 0:
        jugador_x -= 15
    if teclas[pygame.K_RIGHT] and jugador_x < ANCHO - 80:
        jugador_x += 15
    return jugador_x

# Manejo de regalos, actualizando para incluir la penalización del obstáculo
def manejar_regalos(regalos, jugador_x, jugador_y, puntaje, velocidad_regalo, sonido_recoger):
    global tiempo_cambio_imagen, jugador_mostrando_alternativa
    regalos_recogidos = []

    for regalo in regalos:
        regalo["y"] += velocidad_regalo
        if regalo["y"] > ALTO:  # Si un regalo cae fuera de la pantalla
            if regalo["tipo"] == "obstaculo":
                regalos_recogidos.append(regalo)  # El obstáculo cae sin penalizar al jugador
            else:
                return -1  # Si otro tipo de regalo cae, el juego termina

        # Comprobar colisión con el jugador
        if (
            jugador_x < regalo["x"] + 50
            and jugador_x + 80 > regalo["x"]
            and jugador_y < regalo["y"] + 50
            and jugador_y + 80 > regalo["y"]
        ):
            regalos_recogidos.append(regalo)
            if regalo["tipo"] == "obstaculo":
                puntaje -= 2  # Penalización por recoger un obstáculo
                sonido_recoger.play()  # Sonido específico
            else:
                sonido_recoger.play()
                jugador_mostrando_alternativa = True
                tiempo_cambio_imagen = 15
                puntaje += 1 if regalo["tipo"] == "vitamina" else 2

    # Eliminar los regalos que han sido recogidos o han salido de la pantalla
    for regalo in regalos_recogidos:
        regalos.remove(regalo)

    return puntaje

# Generar regalos aleatorios con niveles, incluyendo obstáculos
def generar_regalo(regalos, nivel):
    probabilidad = PROBABILIDADES["niveles"](nivel)
    if random.randint(1, probabilidad) == 1:
        tipo = random.choices(
            ["vitamina", "vitamina1", "obstaculo"],
            weights=[0.4, 0.4, 0.2],  # Ajustar la probabilidad de cada tipo
            k=1
        )[0]
        ruta = {
            "vitamina": RUTAS["vitamina"],
            "vitamina1": RUTAS["vitamina1"],
            "obstaculo": RUTAS["obstaculo"]
        }[tipo]
        regalos.append({
            "x": random.randint(0, ANCHO - 50),
            "y": -50,
            "tipo": tipo,
            "imagen": cargar_imagen(ruta, (50, 50))
        })
    return regalos

# Dibujar elementos
def dibujar_elementos(pantalla, fondo_img, jugador_img, regalos, jugador_x, jugador_y):
    pantalla.blit(fondo_img, (0, 0))
    pantalla.blit(jugador_img, (jugador_x, jugador_y))
    for regalo in regalos:
        pantalla.blit(regalo["imagen"], (regalo["x"], regalo["y"]))

# Mostrar mensaje de victoria
def mostrar_mensaje_victoria(pantalla):
    pantalla.fill((0, 0, 0))  # Limpia la pantalla
    fuente = pygame.font.SysFont(None, 72)
    texto = fuente.render("¡Ya estás listo para enfrentar las cenas Navideñas!", True, (0, 255, 0))
    pantalla.blit(texto, (ANCHO // 2 - 300, ALTO // 2 - 50))
    pygame.display.flip()
    pygame.time.delay(3000)  # Espera 3 segundos antes de continuar

# Inicialización
pantalla = inicializar_pygame()
# Mostrar pantalla de carga
mostrar_pantalla_de_carga(pantalla, RUTAS["carga"])  

# Cargar recursos
fondo_img = cargar_imagen(RUTAS["fondo"], (ANCHO, ALTO))
jugador_img = cargar_imagen(RUTAS["jugador"], (80, 80))
jugador_img_alternativa = cargar_imagen(RUTAS["jugador_alternativo"], (80, 80))
sonido_recoger = cargar_sonidos()
ranking = cargar_ranking()

reloj = pygame.time.Clock()

# Variables de animación del jugador
tiempo_cambio_imagen = 0
jugador_mostrando_alternativa = False

# Bucle principal del juego
# Bucle principal del juego
while True:
    mostrar_menu_inicial(pantalla)

    while True:
        # Iniciar música al comenzar el juego
        pygame.mixer.music.load(RUTAS["musica_fondo"])
        pygame.mixer.music.play(-1)

        # Variables iniciales del juego
        jugador_x, jugador_y = ANCHO // 2, ALTO - 100
        regalos = []
        puntaje = 0
        nivel = 1
        velocidad_regalo = VELOCIDAD_BASE
        jugando = True

        while jugando:
            manejar_eventos()
            teclas = pygame.key.get_pressed()

            if teclas[pygame.K_p]:
                pausado = not pausado
                pygame.time.delay(200)

            if pausado:
                pausar_juego(pantalla)
                continue

            manejar_volumen(teclas)
            jugador_x = mover_jugador(teclas, jugador_x)

            # Calcular nivel y ajustar parámetros
            nivel = calcular_nivel(puntaje)
            velocidad_regalo = VELOCIDAD_BASE + nivel

            regalos = generar_regalo(regalos, nivel)

            resultado = manejar_regalos(regalos, jugador_x, jugador_y, puntaje, velocidad_regalo, sonido_recoger)
            if resultado == -1:  # Si un regalo no deseado cae fuera de la pantalla
                mostrar_game_over(pantalla, puntaje)
                accion = preguntar_reiniciar(pantalla)
                if accion == "menu":
                    jugando = False  # Volver al menú
                    break
                elif accion == "reiniciar":
                    # Salir del bucle interno para reiniciar el juego
                    break

            else:
                puntaje = resultado

            if puntaje >= PUNTAJE_OBJETIVO:
                mostrar_mensaje_victoria(pantalla)
                accion = preguntar_reiniciar(pantalla)
                if accion == "menu":
                    jugando = False  # Volver al menú
                    break
                elif accion == "reiniciar":
                    # Salir del bucle interno para reiniciar el juego
                    break

            if jugador_mostrando_alternativa:
                tiempo_cambio_imagen -= 1
                if tiempo_cambio_imagen <= 0:
                    jugador_mostrando_alternativa = False

            imagen_actual_jugador = jugador_img_alternativa if jugador_mostrando_alternativa else jugador_img

            # Dibujar elementos en pantalla
            dibujar_elementos(pantalla, fondo_img, imagen_actual_jugador, regalos, jugador_x, jugador_y)
            mostrar_puntaje(pantalla, puntaje)
            mostrar_nivel(pantalla, nivel)

            pygame.display.flip()
            reloj.tick(30)

        # Si el usuario selecciona "reiniciar", vuelve a iniciar este bucle
        if not jugando:
            break
