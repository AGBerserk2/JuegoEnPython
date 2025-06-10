# donde se ejecutara la app
from logica import es_movimiento_valido, colocar_pieza, colores_por_jugador, mostrar_tablero
from score import Score
from figuras import piezas
import movimiento  # Importar movimiento para iniciar el juego

# Inicializar el tablero (20x20 para Blokus)
tablero = [[0]*20 for _ in range(20)]

# Inicializar puntajes y jugadores
score = Score()
score.registrar_jugador("Kelvin")
score.registrar_jugador("Ana")

# Piezas disponibles por jugador (10 fichas cada uno)
piezas_por_jugador = {
    "Kelvin": [piezas(i) for i in range(10)],
    "Ana": [piezas(i) for i in range(10)]
}

# Seguimiento del primer movimiento
es_primer_movimiento = {"Kelvin": True, "Ana": True}

# Variables para movimiento.py
x, y = 0, 0
pieza = piezas(0)  # Ficha inicial
colocadas = []  # Lista de piezas colocadas
jugador_actual = "Kelvin"

# Pasar variables a movimiento.py (asumiendo que las usa directamente o tiene una función)
movimiento.tablero = tablero
movimiento.score = score
movimiento.pieza = pieza
movimiento.colocadas = colocadas
movimiento.jugador_actual = jugador_actual
movimiento.piezas_por_jugador = piezas_por_jugador
movimiento.es_primer_movimiento = es_primer_movimiento
movimiento.colores_por_jugador = colores_por_jugador

# Iniciar el juego (asumiendo que movimiento.py tiene su propio bucle)
import os
os.system('python movimiento.py')  # Ejecutar movimiento.py

