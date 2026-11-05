# Neurito

Proyecto educativo de redes neuronales implementadas con NumPy y visualizadas con Pygame. Incluye la mascota original, el juego de salto de obstáculos y un laberinto en el que Neurito aprende a encontrar comida.

## Requisitos

- Python 3.12 o superior.
- [uv](https://docs.astral.sh/uv/) para instalar las dependencias declaradas en el proyecto.

## Instalación

```bash
git clone https://github.com/johnmunoz303/neurito.git
cd neurito
uv sync
```

## Mascota original

```bash
uv run main.py
```

La red recibe hambre, energía y aburrimiento y elige entre comer, dormir y jugar. Usa una arquitectura de 3 entradas, 6 neuronas ocultas con ReLU y 3 salidas con Softmax. El estado tranquilo se determina mediante una regla visual.

Controles: `H/J` cambia el hambre, `E/D` la energía, `A/S` el aburrimiento, `R` genera valores aleatorios, `N` establece el estado tranquilo y `Esc` cierra la ventana. Para mostrar la interfaz en español, cambia `LANGUAGE = "en"` por `LANGUAGE = "es"` en `main.py`.

Los experimentos y la explicación de pesos, sesgos y entrenamiento están en [EXPERIMENTOS.md](EXPERIMENTOS.md).

## Neurito 2.0: salto de obstáculos

```bash
uv run saltar.py
```

La red recibe distancia, velocidad y tiempo estimado hasta el obstáculo. Tiene 12 neuronas ocultas con ReLU y una salida sigmoide que decide entre saltar y esperar. El entrenamiento es supervisado con datos sintéticos, retropropagación y descenso de gradiente.

| Tecla | Acción |
|---|---|
| `1` | Entrenar una época |
| `2` | Entrenar cien épocas |
| `3` | Activar o pausar entrenamiento continuo |
| `A` | Alternar control automático y manual |
| `Espacio` | Saltar en modo manual |
| `C` | Reiniciar pista y contadores |
| `R` | Reiniciar pesos y contadores |
| `Esc` | Salir |

La ventana muestra la pérdida, la precisión de prueba, la puntuación de salto y los contadores de obstáculos y choques. Los pesos se mantienen en memoria durante la ejecución; no se guardan al cerrar.

Consulta [GUIA_SALTO.md](GUIA_SALTO.md) para conocer las etiquetas, la arquitectura y los experimentos propuestos.

## Neurito 3.0: laberinto

```bash
uv run laberinto.py
```

Neurito aprende a moverse en tres mapas a partir de rutas generadas con BFS. El modo puro elige la salida más alta de la red. El modo asistido descarta movimientos contra paredes y penaliza las casillas visitadas. Pulsa **2** para entrenar cien épocas y **A** para cambiar de modo.

Consulta la [guía del laberinto](GUIA_LABERINTO.md) para ver todos los controles y el [informe de experimentos](Informe_experimentos_laberinto.md) para consultar las mediciones y la comparación de DFS, BFS y A*.

Desde la carpeta del proyecto, ejecuta las pruebas y repite las mediciones con estos comandos:

```bash
uv run python -m unittest -v test_laberinto.py
uv run python medir_laberinto.py
```

El primer comando comprueba el modelo y el segundo muestra las mediciones en la terminal.

## Archivos principales

| Archivo | Contenido |
|---|---|
| `main.py` | Mascota original |
| `saltar.py` | Interfaz y entrenamiento del juego de salto |
| `salto_modelo.py` | Red neuronal y generación de datos |
| `salto_juego.py` | Física del salto y colisiones |
| `assets/` | Imágenes de la mascota |
| `EXPERIMENTOS.md` | Experimentos de la versión original |
| `GUIA_SALTO.md` | Guía de la versión de salto |
| `laberinto.py` | Interfaz del juego de laberinto |
| `laberinto_mundo.py` | Mapas, navegación y experto BFS |
| `laberinto_red.py` | Red neuronal del laberinto |
| `test_laberinto.py` | Pruebas del laberinto |
| `medir_laberinto.py` | Repite los siete experimentos |
| `GUIA_LABERINTO.md` | Guía del laberinto |
| `Informe_experimentos_laberinto.md` | Resultados de los experimentos |

## Alcance educativo

Las redes aprenden reglas utilizadas para generar ejemplos sintéticos. Una precisión alta indica que reproducen esas reglas en los datos de prueba; no demuestra comprensión de necesidades reales ni garantiza evitar todos los obstáculos del juego.
