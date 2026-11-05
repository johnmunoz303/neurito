import json
import os
import sys
from collections import deque
from heapq import heappop, heappush
from pathlib import Path

# Put this file in the project folder, or pass that folder as an argument.
proyecto = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent
if not (proyecto / 'laberinto_red.py').is_file():
    raise SystemExit('Indica la carpeta de Neurito: python medir_laberinto.py RUTA_A_NEURITO')
sys.path.insert(0, str(proyecto))
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
import numpy as np
from laberinto_red import RedLaberinto, generar_datos
from laberinto_mundo import MAPAS, libres, distancias_bfs, vecino, valido, elegir_accion, Laberinto

def buscar(mapa, inicio, meta, tipo):
    def h(p):
        return abs(p[0] - meta[0]) + abs(p[1] - meta[1])

    pendientes = deque([(inicio, ())])
    heap = [(h(inicio), (), inicio)]
    mejor = {inicio: 0}
    exploradas = 0
    while heap if tipo == 'A*' else pendientes:
        if tipo == 'A*':
            _, ruta, p = heappop(heap)
            if len(ruta) != mejor[p]:
                continue
        elif tipo == 'BFS':
            p, ruta = pendientes.popleft()
        else:
            p, ruta = pendientes.pop()
        exploradas += 1
        if p == meta:
            return ruta, exploradas
        for a in (range(3, -1, -1) if tipo == 'DFS' else range(4)):
            q = vecino(p, a)
            if not valido(mapa, q):
                continue
            nueva = ruta + (a,)
            if tipo == 'A*':
                if len(nueva) >= mejor.get(q, float('inf')):
                    continue
                mejor[q] = len(nueva)
                heappush(heap, (len(nueva) + h(q), nueva, q))
            elif q not in mejor:
                mejor[q] = len(nueva)
                pendientes.append((q, nueva))
    raise ValueError('Sin ruta')

ent, prueba, casos = generar_datos()
X, y = ent
Xt, yt = prueba
ids = np.array([i for i, _, _, _ in casos])
distancias = {(i, m): distancias_bfs(mapa, m) for i, mapa in enumerate(MAPAS) for m in libres(mapa)}

def evaluar(red, asistido, seleccion=range(len(casos))):
    exitos = choques = ciclos = extra = movimientos = 0
    seleccion = list(seleccion)
    for k in seleccion:
        i, inicio, meta, _ = casos[k]
        mundo = Laberinto(i)
        mundo.posicion, mundo.meta, mundo.visitadas = inicio, meta, {inicio: 1}
        optimo = distancias[i, meta][inicio]
        limite = min(65, 2 * optimo + 8)
        for _ in range(limite):
            accion, _ = elegir_accion(red, mundo, mundo.visitadas, asistido)
            estado = mundo.mover(accion)
            if estado == 'comida':
                exitos += 1
                movimientos += mundo.pasos
                extra += mundo.pasos - optimo
                break
            if estado == 'pared':
                choques += 1
                break
        else:
            ciclos += 1
    return [len(seleccion), exitos, choques, ciclos, round(movimientos / max(exitos, 1), 2), round(extra / max(exitos, 1), 2)]

def entrenar(ocultas=96, tasa=.45, etiquetas=y, etiquetas_prueba=yt, cortes=(0,100,200,400)):
    red = RedLaberinto(ocultas=ocultas, tasa=tasa)
    resultados = {}
    for ep in range(max(cortes)+1):
        if ep:
            red.entrenar_epoca(X, etiquetas)
        if ep in cortes:
            p = red.adelante(X)[2]
            perdida = -np.log(np.clip(p[np.arange(len(p)), etiquetas], 1e-10, 1)).mean()
            resultados[ep] = [round(float(perdida),4), round(100*red.exactitud(Xt, etiquetas_prueba),2),
                             evaluar(red,False), evaluar(red,True)]
    return red, resultados

def mostrar(nombre, datos):
    print(nombre, json.dumps(datos), flush=True)

mostrar('datos', [len(X), len(Xt)])
red, resultados = entrenar()
mostrar('base', resultados)
for i in range(len(MAPAS)):
    mask = ids == i
    indices = np.flatnonzero(mask)
    mostrar(f'mapa {i+1}', [round(100*red.exactitud(Xt[mask],yt[mask]),2),
                           evaluar(red,False,indices), evaluar(red,True,indices)])
for n in (16,32,128):
    _, resultados = entrenar(ocultas=n,cortes=(400,))
    mostrar(f'ocultas {n}', resultados)
for tasa in (.05,1.2):
    _, resultados = entrenar(tasa=tasa,cortes=(100,200,400))
    mostrar(f'tasa {tasa}', resultados)

for algoritmo in ('DFS','BFS','A*'):
    rutas = {}
    for i, mapa in enumerate(MAPAS):
        for meta in libres(mapa):
            for inicio in distancias[i,meta]:
                if inicio != meta:
                    rutas[i,inicio,meta] = buscar(mapa,inicio,meta,algoritmo)
    info = [rutas[i,p,m] for i,p,m,_ in casos]
    propias = np.array([ruta[0] for ruta,_ in info])
    optima = [distancias[i,m][p] for i,p,m,_ in casos]
    longitudes = [len(ruta) for ruta,_ in info]
    mostrar(f'busqueda {algoritmo}', [round(float(np.mean(longitudes)),2),
            round(float(np.mean([visitadas for _,visitadas in info])),2),
            sum(a==b for a,b in zip(longitudes,optima)),
            round(float(np.mean(propias==yt)*100),2)])
    if algoritmo == 'BFS':
        assert np.array_equal(propias,yt)
        continue
    nuevas = np.array([rutas[int(row[:3].argmax()), divmod(int(row[3:84].argmax()),9),
                         divmod(int(row[84:].argmax()),9)][0][0] for row in X])
    _, resultados = entrenar(etiquetas=nuevas,etiquetas_prueba=propias,cortes=(400,))
    mostrar(f'red {algoritmo}', resultados)
