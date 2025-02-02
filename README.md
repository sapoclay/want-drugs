# Yonkie Warrior

## Want Drugs? - Juego creado con Python y Pygame

![want-drugs](https://github.com/user-attachments/assets/e4db4f47-ef83-4e8b-9ca1-f650c1e3ce06)

- "Want Drugs?" es un juego arcade básico desarrollado en Python utilizando la biblioteca Pygame. El objetivo del juego es controlar un personaje que debe recoger regalos mientras esquiva obstáculos. El juego incluye características como pausa, ajuste de volumen, y un sistema de ranking para guardar las mejores puntuaciones. Este juego ha sido causado por las cenas familiares de la navidad ....

## Características

![want-drugs](https://github.com/user-attachments/assets/6bd68345-660d-414e-a343-ce8ddbcb4620)

* Pantalla de carga estática.

* Menú de inicio. Desde ahí se puede "Empezar a jugar", "Ver el repositorio en GitHub" o "Salir".

![yonki-warrior-menu](https://github.com/user-attachments/assets/eb0394c6-e0bb-4522-9169-4371d1850154)

* Las pastillas redondas dan 2 puntos, las alargadas solo 1. Si el usuario recoge la mierda, se le restarán 2 puntos al puntuaje total, por lo que el usuario deberá dejarla pasar.

* El juego se considera terminado al alcanzar los 100 puntos.

* El juego cuenta con niveles de dificultad. Cambia de nivel cada 20 puntos obtenidos. 

* Jugabilidad: Recoge tu medicación para ganar puntos y llegar contento a tu cena navideña.

* Pausa y reanudación: Pulsa P para pausar y reanudar el juego.

* Control de volumen:

        - Pulsa M para silenciar o activar el sonido.

        - Pulsa + o - para ajustar el volumen.

* Sistema de ranking: Guarda las puntuaciones más altas con el nombre del jugador.

* Desde el menú principal ahora se puede visitar este repositorio en GitHub del proyecto o ver las 5 puntuaciones más altas registradas.

* Opciones de reinicio: Al final del juego, puedes elegir volver a jugar.

## Requisitos del Sistema

- Python 3.8 o superior

- Biblioteca Pygame instalada (debería instalarse en el entorno virtual de forma automática al ejecutar run_app.py)

## Archivos requeridos

Asegúrate de que el directorio assets contenga los siguientes subdirectorios y archivos:
```
assets/
├── Img/
│   ├── background.png
│   ├── carga.jpeg
│   ├── obstaculo.png
│   ├── fondo_menu.jpeg
│   ├── personaje.png
│   ├── personaje_alternativo.png
│   ├── personaje_creditos.png
│   ├── vitamina1.png
│   └── vitamina.png
├── Music/
    ├── game_over.mp3
    ├── musica_fondo.mp3
    └── sonido_recoger.mp3
```

## Ejecución del Juego

Para ejecutar el juego, utiliza el script run_app.py que automatiza la configuración del entorno y la ejecución:

```
python run_app.py
```

## Controles

- Flechas izquierda/derecha: Mover el personaje.

- P: Pausar/Reanudar el juego.

- M: Silenciar/Activar sonido.

- Utiliza + / -: Aumentar/Disminuir el volumen (esto todavía no funciona correctamente).

- Al finalizar el juego, el usuario puede seleccionar S / N para jugar de nuevo o salir del juego.

## Sistema de Ranking

El ranking de las mejores puntuaciones se guarda en el archivo ranking.txt. Este archivo se actualiza automáticamente al final de cada partida.

## Desarrollado por

### entreunosyceros

## Licencia

Este proyecto está licenciado bajo la [Licencia MIT](LICENSE).
