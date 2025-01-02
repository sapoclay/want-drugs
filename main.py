import pygame
import random
import sys
import os
from config import *
from menu import mostrar_menu_inicial   
from ranking import cargar_ranking, guardar_ranking

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

def cargar_sonidos():
    pygame.mixer.music.load(RUTAS["musica_fondo"])
    pygame.mixer.music.set_volume(VOLUMEN_INICIAL)
    pygame.mixer.music.play(-1)  # Bucle infinito
    sonido_recoger = pygame.mixer.Sound(RUTAS["sonido_recoger"])
    return sonido_recoger



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

# Funciones de pausa
def pausar_juego(pantalla):
    fuente = pygame.font.SysFont(None, 72)
    texto = fuente.render("Juego en Pausa", True, (255, 255, 0))
    pantalla.blit(texto, (ANCHO // 2 - 200, ALTO // 2 - 50))
    pygame.display.flip()

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
    guardar_ranking()

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

# Mostrar ranking
def mostrar_ranking(pantalla):
    pantalla.fill((0, 0, 0))
    fuente = pygame.font.SysFont(None, 48)
    texto_titulo = fuente.render("Ranking:", True, (255, 255, 0))
    pantalla.blit(texto_titulo, (ANCHO // 2 - 100, 50))

    for i, (nombre, puntaje) in enumerate(ranking[:5]):
        texto = fuente.render(f"{i + 1}. {nombre}: {puntaje}", True, (255, 255, 255))
        pantalla.blit(texto, (ANCHO // 2 - 200, 150 + i * 40))

    pygame.display.flip()
    pygame.time.delay(3000)

# Preguntar reinicio
def preguntar_reiniciar(pantalla):
    fuente = pygame.font.SysFont(None, 48)
    while True:
        pantalla.fill((0, 0, 0))
        texto = fuente.render("¿Quieres jugar de nuevo? (S/N)", True, (255, 255, 255))
        pantalla.blit(texto, (ANCHO // 2 - 200, ALTO // 2 - 50))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_s:
                    return True
                if evento.key == pygame.K_n:
                    return False

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
while True:
    mostrar_menu_inicial(pantalla)

    # Iniciar música al comenzar el juego
    pygame.mixer.music.load(RUTAS["musica_fondo"])
    pygame.mixer.music.play(-1)

    # Variables iniciales del juego
    jugador_x, jugador_y = ANCHO // 2, ALTO - 100
    regalos = []
    puntaje = 0
    nivel = 1
    velocidad_regalo = VELOCIDAD_BASE

    # Bucle principal del juego
    while True:
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
            if not preguntar_reiniciar(pantalla):
                pygame.quit()
                sys.exit()
            else:
                break
        else:
            puntaje = resultado

        if puntaje >= PUNTAJE_OBJETIVO:
            mostrar_mensaje_victoria(pantalla)
            if not preguntar_reiniciar(pantalla):
                pygame.quit()
                sys.exit()
            else:
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