# Neurito

Proyecto educativo de redes neuronales implementadas con NumPy y visualizadas con Pygame. Incluye la mascota original y una segunda experiencia en la que Neurito aprende cuándo saltar obstáculos.

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

## Alcance educativo

Las redes aprenden reglas utilizadas para generar ejemplos sintéticos. Una precisión alta indica que reproducen esas reglas en los datos de prueba; no demuestra comprensión de necesidades reales ni garantiza evitar todos los obstáculos del juego.
