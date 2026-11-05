# Neurito 2.0: aprende a saltar obstáculos

Neurito aprende **cuándo saltar** ante obstáculos que se aproximan con diferentes velocidades. El cerebro se implementa manualmente con NumPy y el aprendizaje puede observarse en Pygame.

## ¿Qué aprende?

La red recibe tres características normalizadas: distancia al obstáculo, velocidad y tiempo estimado hasta alcanzarlo (distancia / velocidad). La última es una característica derivada, no una observación independiente.

La arquitectura es **3 → 12 → 1**: doce neuronas ocultas con ReLU y una salida con sigmoide. La última devuelve una puntuación entre cero y uno que, con el umbral 0.5, determina si Neurito debe saltar cuando está en el suelo.

## ¿Cómo aprende?

Aplicamos **aprendizaje supervisado**, no aprendizaje por refuerzo. Creamos datos sintéticos que incluyen ejemplos donde es conveniente saltar y otros donde debe esperar. Para generar las etiquetas, definimos una ventana de referencia: saltar cuando el tiempo estimado está entre **7 y 13 fotogramas**. No es una regla aprendida por recompensa ni garantiza evitar choques en todas las situaciones.

La red ajusta sus pesos a partir de la **entropía cruzada binaria**, la **retropropagación** y el **descenso de gradiente**:

`W_nuevo = W_anterior - tasa_de_aprendizaje * gradiente`

El conjunto de entrenamiento equilibra aproximadamente las dos decisiones. De otra manera, una red podría aparentar buena precisión diciendo casi siempre «esperar».

La precisión se mide sobre ejemplos distintos de los utilizados en el entrenamiento. **Una precisión alta no garantiza un buen resultado en el juego**, que también depende de la física del salto.

## Archivos

```text
Neurito/
├── main.py                 # Mascota original: comer, dormir, jugar
├── salto_modelo.py         # Red neuronal manual y datos de entrenamiento
├── salto_juego.py          # Física y detección de colisiones
├── saltar.py               # Juego y visualización del entrenamiento
├── GUIA_SALTO.md
└── assets/
    └── jugar_1.png        # Reutilizado en el nuevo juego
```

## Ejecución

```bash
uv sync
uv run saltar.py
```

No se necesitan dependencias nuevas: se reutilizan NumPy y Pygame.

## Controles

| Tecla | Función |
|---|---|
| `1` | Entrenar una época |
| `2` | Entrenar cien épocas |
| `3` | Activar o pausar entrenamiento continuo |
| `A` | Alternar control automático y manual |
| `Espacio` | Saltar manualmente |
| `C` | Reiniciar pista y contadores |
| `R` | Reiniciar pesos y contadores |
| `Esc` | Salir |

## Experimentos y resultados

Usé 5.000 ejemplos sintéticos para entrenar y 1.500 ejemplos independientes para medir la precisión. Fijé las semillas de los pesos (42), los datos de entrenamiento (123) y los de prueba (456). En cada medición probé el modo automático en 30 intentos independientes, con las mismas velocidades para todos los modelos (5,5 px por fotograma en el primero y otras 29 entre 4,5 y 8,5). Ejecuté la lógica de salto y colisiones del juego sin abrir la ventana. Cada intento termina cuando el obstáculo se esquiva o se produce un choque.

La configuración de referencia usa 12 neuronas ocultas, tasa de aprendizaje de 0,8 y una ventana de 7 a 13 fotogramas. La pérdida se calculó sobre el conjunto de entrenamiento con los pesos del momento de cada medición. Los resultados corresponden a una ejecución por configuración.

### 1. Juego sin entrenar

Con cero épocas, Neurito **esquivó 0 obstáculos y chocó 30 veces**. La red acertó el 45,00 % de las etiquetas de prueba. Con los pesos iniciales, sus decisiones no coincidieron con el momento necesario para esquivar ninguno de los obstáculos probados.

### 2. Entrenamiento de cien en cien épocas

| Épocas | Pérdida | Precisión de prueba | Esquivados | Choques |
|---:|---:|---:|---:|---:|
| 0 | 0,7118 | 45,00 % | 0 | 30 |
| 100 | 0,2547 | 91,33 % | 28 | 2 |
| 200 | 0,2269 | 92,20 % | 30 | 0 |
| 300 | 0,2072 | 92,33 % | 30 | 0 |
| 400 | 0,1847 | 92,47 % | 30 | 0 |
| 500 | 0,1545 | 92,67 % | 30 | 0 |
| 600 | 0,1219 | 95,07 % | 30 | 0 |
| 700 | 0,0970 | 96,07 % | 30 | 0 |
| 800 | 0,0805 | 97,13 % | 30 | 0 |
| 900 | 0,0691 | 97,53 % | 30 | 0 |
| 1.000 | 0,0610 | 98,07 % | 30 | 0 |
| 1.100 | 0,0547 | 98,40 % | 30 | 0 |
| 1.200 | 0,0498 | 98,60 % | 30 | 0 |

La mejora en el juego se vio en las primeras 200 épocas. Después, la red siguió reduciendo la pérdida y acertando más etiquetas, mientras el resultado en la pista se mantuvo en 30 de 30.

### 3. Cambiar la cantidad de neuronas ocultas

Mantuve la tasa en 0,8, entrené 1.200 épocas y comparé los modelos con los mismos datos de prueba.

| Neuronas ocultas | Pérdida | Precisión de prueba | Esquivados | Choques |
|---:|---:|---:|---:|---:|
| 3 | 0,1961 | 93,33 % | 30 | 0 |
| 12 | 0,0498 | 98,60 % | 30 | 0 |
| 24 | 0,0430 | 98,80 % | 30 | 0 |

Con 3 neuronas la red acertó menos etiquetas nuevas, aunque resolvió los 30 intentos. Con 24 neuronas, la precisión subió solo 0,20 puntos porcentuales respecto a 12 y el resultado en la pista fue el mismo. Para estas pruebas, 12 neuronas fueron suficientes.

### 4. Cambiar la tasa de aprendizaje

Mantuve 12 neuronas ocultas y la ventana de 7 a 13 fotogramas.

| Tasa | Pérdida a 100 épocas | Pérdida a 400 épocas | Pérdida a 1.200 épocas | Precisión final | Esquivados / choques al final |
|---:|---:|---:|---:|---:|---:|
| 0,01 | 0,6455 | 0,5390 | 0,4085 | 87,07 % | 13 / 17 |
| 0,8 | 0,2547 | 0,1847 | 0,0498 | 98,60 % | 30 / 0 |
| 1,2 | 0,2610 | 0,1471 | 0,0332 | 99,13 % | 30 / 0 |

La tasa de 0,01 redujo la pérdida lentamente y todavía produjo 17 choques al final. La de 0,8 tuvo una pérdida un poco menor que 1,2 a las 100 épocas. A partir del corte de 400, la de 1,2 obtuvo menor pérdida y terminó con la mejor precisión de las tres tasas. Ambas esquivaron los 30 obstáculos al final.

### 5. Cambiar la ventana de salto

Cambié los límites de la regla que genera las etiquetas y moví también el intervalo donde se generan los ejemplos positivos. Entrené cada modelo durante 1.200 épocas con 12 neuronas y tasa de 0,8. Además, probé la regla directamente en el juego para separar el efecto de la ventana del error de la red.

| Ventana (fotogramas) | Pérdida | Precisión frente a su propia regla | Red: esquivados / choques | Regla directa: esquivados / choques |
|---|---:|---:|---:|---:|
| 7 a 13 | 0,0498 | 98,60 % | 30 / 0 | 30 / 0 |
| 9 a 15 | 0,0470 | 98,33 % | 30 / 0 | 30 / 0 |
| 2 a 5 | 0,0840 | 96,73 % | 30 / 0 | 30 / 0 |
| 30 a 36 | 0,0423 | 98,40 % | 0 / 30 | 0 / 30 |

Las primeras tres ventanas funcionaron para las velocidades probadas. Con 30 a 36 fotogramas, el salto se inicia demasiado pronto y Neurito ya está demasiado bajo cuando llega al obstáculo. Como aplicar la regla directamente también dio 30 choques, el problema en ese caso está en la política usada para etiquetar los datos.

### Pregunta central

**¿Por qué una red puede clasificar ejemplos con buena precisión y aun así chocar?**

La precisión mide cuántas veces coincide con las etiquetas de ejemplos aislados. En el juego, un error en el momento decisivo puede causar un choque aunque haya acertado en muchos otros fotogramas. Además, las etiquetas pueden enseñar una regla que no funciona con la física. Con la ventana de 30 a 36 fotogramas, Neurito acertó el 98,40 % de las etiquetas y chocó 30 de 30 veces. Para evaluar si aprende a esquivar, conviene medir tanto la precisión como los obstáculos esquivados y los choques.
