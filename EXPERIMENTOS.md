# Experimentos con Neurito

Neurito decide entre **comer, dormir y jugar** a partir de su hambre, energía y aburrimiento. Para dormir se toma en cuenta el cansancio, que se calcula como `1 - energía`. Todos estos valores van de 0 a 1.

Para estas pruebas usé el entrenamiento de `main.py`, sin abrir la ventana del personaje. Se mantuvieron los 3.000 ejemplos de entrenamiento y la semilla 42. Comparé todas las configuraciones con los mismos 1.000 ejemplos nuevos, generados con semilla 123. La pérdida indica cuánto se equivoca el modelo: cuanto más baja, mejor. La precisión indica el porcentaje de decisiones que coinciden con la regla usada para crear los ejemplos.

## 1. Mantener dos necesidades fijas y cambiar la tercera

Dejé la energía en 0,50 y el aburrimiento en 0,20. Luego cambié solamente el hambre, usando el modelo original de 6 neuronas.

| Hambre | Comer | Dormir | Jugar | Acción predicha |
|---|---|---|---|---|
| 0,40 | 13,32 % | 86,44 % | 0,24 % | Dormir |
| 0,50 | 49,89 % | 49,98 % | 0,13 % | Dormir, por muy poco |
| 0,60 | 86,58 % | 13,39 % | 0,03 % | Comer |

La acción cambia cerca de un hambre de 0,50. Tiene sentido porque la energía de 0,50 equivale a un cansancio de 0,50: al superar ese nivel, comer empieza a tener más prioridad que dormir. Estos puntos muestran dónde ocurre aproximadamente el cambio, no su valor exacto.

La red aprendió a aproximar la regla, así que no siempre resuelve los empates exactamente como ella. La regla que crea las etiquetas elige la primera acción en caso de empate: comer antes que dormir y dormir antes que jugar.

## 2. Comparar prioridades casi iguales

| Hambre | Energía | Aburrimiento | Comer | Dormir | Jugar |
|---|---|---|---|---|---|
| 0,49 | 0,50 | 0,49 | 32,93 % | 37,78 % | 29,29 % |
| 0,50 | 0,50 | 0,50 | 35,21 % | 33,45 % | 31,34 % |
| 0,51 | 0,50 | 0,50 | 39,66 % | 31,25 % | 29,09 % |

Cuando las necesidades están casi empatadas, Softmax reparte los porcentajes de forma más parecida. Un cambio pequeño puede cambiar la acción ganadora, aunque las otras opciones sigan teniendo bastante peso. Si una necesidad domina claramente, su porcentaje puede acercarse al 100 %.

En otras palabras, elegir una acción no significa que la red esté completamente segura. Estos porcentajes son las salidas del modelo; no garantizan que representen una certeza real.

## 3. Cambiar la cantidad de neuronas ocultas

Mantuve 1.200 épocas y una tasa de aprendizaje de 0,1.

| Neuronas ocultas | Pérdida final en entrenamiento | Precisión en prueba |
|---|---|---|
| 3 | 0,1618 | 96,3 % |
| 6 | 0,1224 | 99,4 % |
| 10 | 0,1261 | 99,1 % |
| 20 | 0,1220 | 99,0 % |

Con 3 neuronas el modelo pudo aprender, pero cometió más errores. Con 6 obtuvo la mejor precisión de esta comparación. Pasar a 10 o 20 no dio una mejora clara: para una regla tan sencilla, tener más neuronas no asegura mejores resultados.

Estos resultados corresponden a una ejecución por configuración. Para afirmar que una opción es siempre mejor habría que repetir el experimento con distintas semillas.

## 4. Cambiar las épocas o la tasa de aprendizaje

Una época es una vuelta de entrenamiento con todos los ejemplos. La tasa de aprendizaje marca el tamaño de los ajustes que hace la red.

### Más o menos épocas

Con 6 neuronas y tasa de 0,1:

| Épocas | Pérdida final en entrenamiento | Precisión en prueba |
|---|---|---|
| 100 | 0,8059 | 75,1 % |
| 400 | 0,2644 | 97,5 % |
| 1.200 | 0,1224 | 99,4 % |
| 3.000 | 0,0710 | 99,7 % |

Entrenar más mejoró el resultado, pero cada vez aportó menos. Entre 100 y 400 épocas hubo un cambio grande; entre 1.200 y 3.000 la mejora de precisión fue pequeña. En estas pruebas no hubo un estancamiento completo, aunque sí rendimientos cada vez menores.

### Ajustes más pequeños o más grandes

Con 6 neuronas y 1.200 épocas:

| Tasa de aprendizaje | Pérdida final en entrenamiento | Precisión en prueba |
|---|---|---|
| 0,01 | 0,7372 | 80,1 % |
| 0,1 | 0,1224 | 99,4 % |
| 1 | 0,0447 | 98,4 % |
| 10 | 3,0699 | 33,3 % |

Con 0,01 el aprendizaje avanzó lentamente. Con 0,1 hubo una mejora estable. Con 1 la pérdida final fue menor, pero hubo subidas y bajadas durante el entrenamiento y la precisión de prueba quedó por debajo de la obtenida con 0,1. Esto muestra que una pérdida de entrenamiento menor no siempre significa acertar más con ejemplos nuevos.

Con 10 los ajustes fueron demasiado grandes: la pérdida osciló y el resultado quedó cerca de acertar una de cada tres decisiones. En esta prueba, el entrenamiento se volvió inestable.

## 5. ¿Qué datos y etiquetas requeriría una cuarta acción?

Una opción sería enseñar a Neurito a **descansar tranquilo** cuando ninguna necesidad sea urgente.

Haría falta incluir ejemplos con hambre baja, energía alta y aburrimiento bajo, y etiquetarlos como «tranquilo». Por ejemplo: hambre 0,20, energía 0,90 y aburrimiento 0,20. También harían falta ejemplos de las otras tres acciones y situaciones cercanas al límite entre estar tranquilo y necesitar hacer algo.

Podría usarse la regla que ya aparece en la pantalla: tranquilo si el hambre es menor que 0,40, la energía mayor que 0,60 y el aburrimiento menor que 0,40. Los demás ejemplos seguirían etiquetándose según la necesidad más alta. Conviene incluir suficientes ejemplos de cada acción para que la nueva no quede poco representada.

Además de los datos, habría que ampliar la salida de la red de 3 a 4 opciones y volver a entrenar. Para esta acción bastan las tres entradas actuales. Si se quisiera añadir «beber», por ejemplo, también sería útil medir la sed.

**Actualmente, el estado tranquilo es una regla visual del programa. La red solo aprendió comer, dormir y jugar.**

## Explicación de los resultados

### 1. ¿En qué se diferencian pesos y sesgos?

Los pesos indican cuánto influye cada señal en lo que aprende la red. Por ejemplo, ayudan a relacionar un nivel alto de hambre con la decisión de comer.

Los sesgos ajustan el punto desde el que responde cada neurona, como mover el punto de inicio de una balanza. Ambos se van ajustando durante el entrenamiento.

### 2. ¿Por qué el cansancio es `1 - energía`?

Porque en este proyecto se consideran opuestos: a más energía, menos cansancio. Si la energía es 0,90, el cansancio es 0,10; si la energía baja a 0,20, el cansancio sube a 0,80.

Así se pueden comparar hambre, cansancio y aburrimiento con la misma idea: un valor más alto representa una necesidad más urgente. Es una simplificación útil para el juego.

### 3. ¿Qué hace ReLU y qué hace Softmax?

**ReLU** deja pasar los valores positivos y convierte los negativos en cero. Se usa en la capa oculta y permite que la red aprenda relaciones más flexibles.

**Softmax** convierte los valores finales en porcentajes que suman 100 %. Así podemos comparar cuánto favorece la red comer, dormir o jugar. El programa elige la acción con el porcentaje más alto.

### 4. ¿Por qué una precisión alta puede ser engañosa?

En este proyecto, los ejemplos se inventan siguiendo una regla sencilla. Alcanzar un 99,4 % significa que la red reproduce muy bien esa regla en los ejemplos de prueba. No demuestra que comprenda necesidades reales ni que vaya a funcionar igual en cualquier situación.

También puede ocultar errores en casos difíciles, como los empates. Y si hubiera muchos más ejemplos de una acción que de las demás, se podría obtener una precisión aparentemente buena acertando sobre todo la acción más frecuente.

Por eso conviene probar casos cercanos a los límites, revisar los errores de cada acción y usar ejemplos distintos de los del entrenamiento. La precisión es una pista útil, pero no cuenta toda la historia.
