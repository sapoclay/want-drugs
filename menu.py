import pygame
import sys
from config import ANCHO, ALTO, RUTAS
from ranking import cargar_ranking, mostrar_ranking


# Función para mostrar los créditos
def mostrar_creditos(pantalla):
    # Cargar la imagen para los créditos
    try:
        imagen_creditos = pygame.image.load(RUTAS["creditos_imagen"])
        imagen_creditos = pygame.transform.scale(imagen_creditos, (300, 300))  # Tamaño ajustado
    except pygame.error as e:
        print(f"Error al cargar la imagen de créditos: {e}")
        pygame.quit()
        sys.exit()

    fuente_titulo = pygame.font.SysFont(None, 48)
    fuente_pequeña = pygame.font.SysFont(None, 32)

    texto_creditos1 = "Desarrollado por:"
    texto_creditos2 = "entreunosyceros"
    texto_instrucciones = "Pulsa Esc para volver al menú"

    while True:
        pantalla.fill((0, 0, 0))  # Fondo negro

        # Mostrar la imagen centrada
        ancho_img, alto_img = imagen_creditos.get_size()
        pantalla.blit(imagen_creditos, ((ANCHO - ancho_img) // 2, (ALTO - alto_img) // 2 - 100))

        # Mostrar el texto principal
        texto1 = fuente_titulo.render(texto_creditos1, True, (255, 255, 255))
        texto2 = fuente_titulo.render(texto_creditos2, True, (255, 255, 255))
        ancho_texto1, alto_texto1 = texto1.get_size()
        ancho_texto2, alto_texto2 = texto2.get_size()
        pantalla.blit(texto1, ((ANCHO - ancho_texto1) // 2, (ALTO + alto_img) // 2 - 50))
        pantalla.blit(texto2, ((ANCHO - ancho_texto2) // 2, (ALTO + alto_img) // 2))

        # Mostrar el texto de instrucciones
        texto3 = fuente_pequeña.render(texto_instrucciones, True, (255, 255, 0))
        ancho_texto3, alto_texto3 = texto3.get_size()
        pantalla.blit(texto3, ((ANCHO - ancho_texto3) // 2, (ALTO + alto_img) // 2 + alto_texto2 + 20))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:  # Volver al menú principal
                    return

# Función para mostrar un mensaje en pantalla
def mostrar_mensaje(pantalla, mensaje, color=(255, 255, 255)):
    pantalla.fill((0, 0, 0))
    fuente = pygame.font.SysFont(None, 48)
    texto = fuente.render(mensaje, True, color)
    ancho_texto, alto_texto = texto.get_size()
    pantalla.blit(texto, ((ANCHO - ancho_texto) // 2, (ALTO - alto_texto) // 2))
    pygame.display.flip()
    pygame.time.delay(3000)

# Función para mostrar el ranking o un mensaje si no hay datos
def ver_ranking(pantalla):
    ranking = cargar_ranking()
    if not ranking:
        mostrar_mensaje(pantalla, "No hay puntuaciones registradas.", (255, 0, 0))
    else:
        mostrar_ranking(pantalla)

# Función para mostrar el menú inicial
def mostrar_menu_inicial(pantalla):
    opciones = ["Empezar a jugar", "Ver puntuaciones", "Ver repositorio en GitHub", "Créditos", "Salir"]
    opcion_seleccionada = 0  # Índice de la opción seleccionada

    # Cargar la imagen de fondo
    try:
        fondo = pygame.image.load(RUTAS["fondo_menu"])
        fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))  # Ajustar al tamaño de la pantalla
    except pygame.error as e:
        print(f"Error al cargar la imagen de fondo: {e}")
        pygame.quit()
        sys.exit()

    while True:
        pantalla.blit(fondo, (0, 0))  # Dibujar la imagen de fondo

        fuente = pygame.font.SysFont(None, 48)
        for i, opcion in enumerate(opciones):
            color = (255, 255, 0) if i == opcion_seleccionada else (255, 255, 255)
            texto = fuente.render(opcion, True, color)
            pantalla.blit(texto, (ANCHO // 2 - 150, ALTO // 2 - 60 + i * 60))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    opcion_seleccionada = (opcion_seleccionada - 1) % len(opciones)
                elif evento.key == pygame.K_DOWN:
                    opcion_seleccionada = (opcion_seleccionada + 1) % len(opciones)
                elif evento.key == pygame.K_RETURN:  # Seleccionar opción
                    if opcion_seleccionada == 0:  # Empezar a jugar
                        return
                    elif opcion_seleccionada == 1:  # Ver Ranking
                        ver_ranking(pantalla)
                    elif opcion_seleccionada == 2:  # Ver repositorio en GitHub
                        import webbrowser
                        webbrowser.open("https://github.com/sapoclay/want-drugs")
                    elif opcion_seleccionada == 3:  # Créditos
                        mostrar_creditos(pantalla)
                    elif opcion_seleccionada == 4:  # Salir
                        pygame.quit()
                        sys.exit()
