# Dimensiones de la pantalla
ANCHO, ALTO = 800, 600

# Velocidad base de los regalos
VELOCIDAD_BASE = 4

# Estado inicial del juego
pausado = False
muteado = False  # Estado inicial de mute
ranking = []  # Inicializar ranking

# Volumen inicial
VOLUMEN_INICIAL = 0.3

# Rutas de recursos
RUTAS = {
    "musica_fondo": 'assets/Music/musica_fondo.mp3',
    "sonido_recoger": 'assets/Music/sonido_recoger.mp3',
    "game_over": 'assets/Music/game_over.mp3',
    "fondo": 'assets/Img/background.png',
    "jugador": 'assets/Img/personaje.png',
    "jugador_alternativo": 'assets/Img/personaje_alternativo.png',
    "vitamina": 'assets/Img/vitamina.png',
    "vitamina1": 'assets/Img/vitamina1.png',
    "obstaculo": 'assets/Img/obstaculo.png',
    "fondo_menu": 'assets/Img/fondo_menu.jpeg',
    "carga": 'assets/Img/carga.jpeg'
}

# Probabilidades y penalizaciones
PROBABILIDADES = {
    "niveles": lambda nivel: max(50 - nivel * 5, 5),
    "tipos_regalos": {
        "vitamina": 0.4,
        "vitamina1": 0.3,
        "obstaculo": 0.2
    },
    "penalizacion_obstaculo": -2
}

# Otros ajustes
TIEMPO_CAMBIO_IMAGEN = 15
MOVIMIENTO_JUGADOR = 10
PUNTAJE_OBJETIVO = 100
