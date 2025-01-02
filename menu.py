import pygame
import sys
from config import ANCHO, ALTO, RUTAS

# Función para mostrar el menú inicial
def mostrar_menu_inicial(pantalla):
    opciones = ["Empezar a jugar", "Ver repositorio en GitHub", "Salir"]
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
                    elif opcion_seleccionada == 1:  # Ver repositorio en GitHub
                        import webbrowser
                        webbrowser.open("https://github.com/sapoclay/want-drugs")
                    elif opcion_seleccionada == 2:  # Salir
                        pygame.quit()
                        sys.exit()