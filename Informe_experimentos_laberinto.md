# Neurito 3.0 · Experimentos en el laberinto

## Cómo hice la comparación

Usé los tres mapas del proyecto y la división con semilla 42: **2.860 ejemplos de entrenamiento y 716 de prueba**. Cada ejemplo de prueba corresponde a una combinación de mapa, inicio y meta que quedó fuera del entrenamiento. Los tres mapas sí aparecen en ambos conjuntos.

Simulé los recorridos con las funciones del juego, sin abrir Pygame. Cada recorrido terminó al llegar a la comida, al primer intento de cruzar una pared o al agotar un límite de intentos de dos veces la distancia óptima más ocho, con un máximo de 65. Conté los pasos válidos de los recorridos que llegaron. La precisión mide el porcentaje de movimientos que coinciden con la etiqueta del experto, mientras que las llegadas miden recorridos completos. Hice una ejecución por configuración con semilla 42.

## 1. ¿Por qué se atasca sin entrenar?

Sin entrenar, la red pura llegó **22 de 716 veces**. En 589 recorridos intentó cruzar una pared y en 105 agotó el límite. Con los pesos iniciales, la red todavía no ha aprendido a asociar una posición y una meta con el movimiento correcto. Si elige una pared, la posición queda igual y vuelve a producir la misma salida. También puede pasar de una casilla a otra y volver al punto de partida.

## 2. ¿Qué cambió a las 100, 200 y 400 épocas?

Usé 96 neuronas ocultas y una tasa de aprendizaje de 0,45. La pérdida se calculó sobre el conjunto de entrenamiento con los pesos de cada corte.

| Épocas | Pérdida | Precisión de prueba | Llegadas con red pura | Choques | Agotaron el límite | Pasos medios al llegar |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 1,3950 | 27,65 % | 22 | 589 | 105 | 1,82 |
| 100 | 0,1650 | 84,92 % | 367 | 15 | 334 | 5,54 |
| 200 | 0,0414 | 90,08 % | 582 | 5 | 129 | 6,01 |
| 400 | 0,0108 | 91,48 % | 592 | 3 | 121 | 6,04 |

El mayor aumento de llegadas ocurrió antes de las 200 épocas. De 200 a 400, la pérdida siguió bajando y hubo diez llegadas adicionales. El promedio de pasos se calcula solo entre los recorridos exitosos, así que compara grupos distintos. A las 400 épocas, los recorridos exitosos quedaron, en promedio, a solo 0,04 pasos por encima de la ruta óptima de esos mismos casos.

## 3. ¿Qué hace la red y qué aporta la asistencia?

| Épocas | Llegadas con red pura | Llegadas con asistencia |
| ---: | ---: | ---: |
| 0 | 22 / 716 | 412 / 716 |
| 100 | 367 / 716 | 701 / 716 |
| 200 | 582 / 716 | 708 / 716 |
| 400 | 592 / 716 | 713 / 716 |

La red genera cuatro puntuaciones. En modo puro se elige la más alta. En modo asistido, el programa elimina los movimientos contra paredes y resta 0,35 por cada visita previa a la casilla candidata. La mejora de 592 a 713 llegadas a las 400 épocas se obtuvo con los mismos pesos. La diferencia viene de cómo esas reglas usan las puntuaciones del modelo. El modo asistido tuvo cero choques en los cuatro cortes.

## 4. ¿Qué pasó al cambiar las neuronas ocultas?

Mantuve la tasa en 0,45 y entrené 400 épocas en cada prueba.

| Neuronas | Pérdida | Precisión de prueba | Llegadas con red pura | Llegadas con asistencia |
| ---: | ---: | ---: | ---: | ---: |
| 16 | 0,0420 | 87,15 % | 532 | 709 |
| 32 | 0,0162 | 89,25 % | 561 | 704 |
| 96 | 0,0108 | 91,48 % | 592 | 713 |
| 128 | 0,0102 | 90,78 % | 611 | 707 |

En esta ejecución, 96 neuronas lograron la mayor precisión y la mayor cantidad de llegadas con asistencia. Con 128 neuronas, la red pura completó 19 recorridos más que con 96, aunque coincidió menos veces con las etiquetas. El mejor tamaño depende de la métrica que se quiera mejorar.

## 5. ¿Cómo afectó la tasa de aprendizaje?

Mantuve 96 neuronas y las etiquetas de BFS.

| Tasa | Pérdida a 100 épocas | A 200 | A 400 | Precisión final | Llegadas puras / asistidas |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0,05 | 0,6036 | 0,4403 | 0,2814 | 83,24 % | 330 / 701 |
| 0,45 | 0,1650 | 0,0414 | 0,0108 | 91,48 % | 592 / 713 |
| 1,2 | 0,0227 | 0,0058 | 0,0021 | 93,85 % | 617 / 711 |

La pérdida bajó en los tres cortes para cada tasa. Con 0,05 el aprendizaje fue más lento. Con 1,2 la pérdida bajó más rápido y la red pura obtuvo más llegadas que con 0,45. Con asistencia, 0,45 completó dos recorridos más.

## 6. ¿Qué pasó al cambiar de mapa?

Evalué la misma red de 400 épocas por separado en cada mapa.

| Mapa | Precisión de prueba | Llegadas con red pura | Llegadas con asistencia |
| ---: | ---: | ---: | ---: |
| 1 | 92,38 % | 180 / 210 | 210 / 210 |
| 2 | 90,04 % | 197 / 251 | 248 / 251 |
| 3 | 92,16 % | 215 / 255 | 255 / 255 |

El mapa 2 tuvo la menor proporción de llegadas con red pura y concentró los tres recorridos que el modo asistido dejó sin completar. Estos datos miden generalización a nuevos pares de inicio y meta dentro de mapas conocidos. Para medir el desempeño en un mapa desconocido haría falta representarlo mediante sus paredes y reservar mapas completos para la prueba.

## 7. ¿Cómo cambia Neurito con DFS, BFS y A*?

Implementé una comparación aparte con los mismos pares de inicio y meta. DFS usa una pila, BFS una cola y A* prioriza el costo acumulado más la distancia Manhattan a la meta. Primero medí las rutas completas que devuelve cada búsqueda. Después entrené tres redes con la primera acción de la ruta de su experto como etiqueta, con 96 neuronas, tasa de 0,45 y 400 épocas.

| Experto | Longitud media de ruta | Casillas procesadas por búsqueda, en promedio | Rutas óptimas |
| --- | ---: | ---: | ---: |
| DFS | 11,08 | 18,51 | 274 / 716 |
| BFS | 6,06 | 18,49 | 716 / 716 |
| A* | 6,06 | 8,60 | 716 / 716 |

La exploración se midió en búsquedas independientes desde cada inicio hasta su meta. El generador original de BFS puede reutilizar un cálculo de distancias para varios inicios con la misma meta, por lo que el conteo por consulta no mide el tiempo total de generación de etiquetas.

| Experto usado para entrenar | Precisión frente a sus etiquetas | Llegadas con red pura | Llegadas con asistencia |
| --- | ---: | ---: | ---: |
| DFS | 94,83 % | 82 / 716 | 256 / 716 |
| BFS | 91,48 % | 592 / 716 | 713 / 716 |
| A* | 92,60 % | 601 / 716 | 714 / 716 |

DFS encontró rutas más largas. Además, una ruta completa calculada por DFS puede llegar, pero al recalcular desde la siguiente casilla su primer paso puede volver hacia atrás. Imitar esas decisiones por separado puede crear ciclos. La red de DFS acertó el 94,83 % de sus etiquetas y aun así completó solo 82 recorridos en modo puro.

BFS y A* encontraron rutas mínimas en todos los casos. A* procesó menos casillas en esta comparación por consulta y su red completó nueve recorridos puros más en esta ejecución. Los dos expertos pueden elegir primeros movimientos distintos cuando hay más de una ruta mínima. Por eso cada precisión se calculó frente a las etiquetas de su propio experto.

## Verificación

Pasaron las cinco pruebas de test_laberinto.py, incluidas la separación de datos, la corrección de las rutas BFS y la llegada a metas reservadas.

## Cómo repetir las mediciones

Descarga el archivo medir_laberinto.py y cópialo a la carpeta de Neurito, junto a laberinto_red.py y laberinto_mundo.py. Abre PowerShell en esa carpeta y ejecuta:

    uv sync
    uv run python medir_laberinto.py

El script imprime los resultados de los siete experimentos. Las filas de cada corte contienen pérdida, precisión y el resultado de ambos modos. En cada modo, los valores son casos, llegadas, choques, casos que agotaron el límite, pasos medios al llegar y pasos medios por encima de la ruta óptima. Las filas de búsqueda muestran longitud media, casillas procesadas, número de rutas óptimas y coincidencia del primer movimiento con BFS.
