from figuras import piezas
from figuras import rotar_pieza
import os
import time
import keyboard

TABLERO_ALTO = 20
TABLERO_ANCHO = 20

class Score:
    def __init__(self):
        self.puntos_por_jugador = {}

    def registrar_jugador(self, jugador_nombre):
        self.puntos_por_jugador[jugador_nombre] = 0

    def sumar_puntos_por_pieza(self, jugador_nombre, pieza):
        puntos = sum(celda == 1 for fila in pieza for celda in fila)
        self.puntos_por_jugador[jugador_nombre] += puntos

    def obtener_puntos(self, jugador_nombre):
        return self.puntos_por_jugador.get(jugador_nombre, 0)

x, y = 0, 0
pieza = piezas(5)
colocadas = []

score = Score()
score.registrar_jugador("Jugador 1")
score.registrar_jugador("Jugador 2")

jugador_actual = "Jugador 1"  # Empieza Jugador 1

def dibujar_tablero(x, y, pieza, colocadas, score, jugador_actual):
    os.system('cls' if os.name == 'nt' else 'clear')
    
    tablero = [['⬜' for _ in range(TABLERO_ANCHO)] for _ in range(TABLERO_ALTO)]

    # Dibujar piezas colocadas
    for p_colocada, px, py in colocadas:
        for i in range(len(p_colocada)):
            for j in range(len(p_colocada[0])):
                if p_colocada[i][j] == 1:
                    if 0 <= py + i < TABLERO_ALTO and 0 <= px + j < TABLERO_ANCHO:
                        tablero[py + i][px + j] = '🟩'

    # Dibujar pieza actual
    for i in range(len(pieza)):
        for j in range(len(pieza[0])):
            if pieza[i][j] == 1:
                if 0 <= y + i < TABLERO_ALTO and 0 <= x + j < TABLERO_ANCHO:
                    tablero[y + i][x + j] = '🟦'

    # Mostrar el tablero
    for fila in tablero:
        print(''.join(fila))

    print(f"\nTurno de: {jugador_actual}")
    print("Puntaje Jugador 1:", score.obtener_puntos("Jugador 1"))
    print("Puntaje Jugador 2:", score.obtener_puntos("Jugador 2"))

while True:
    dibujar_tablero(x, y, pieza, colocadas, score, jugador_actual)
    time.sleep(0.1)

    if keyboard.is_pressed('esc'):
        break
    elif keyboard.is_pressed('left') and x > 0:
        x -= 1
    elif keyboard.is_pressed('right') and x + len(pieza[0]) < TABLERO_ANCHO:
        x += 1
    elif keyboard.is_pressed('up') and y > 0:
        y -= 1
    elif keyboard.is_pressed('down') and y + len(pieza) < TABLERO_ALTO:
        y += 1
    elif keyboard.is_pressed("r"):
        nueva = rotar_pieza(pieza)
        if x + len(nueva[0]) <= TABLERO_ANCHO and y + len(nueva) <= TABLERO_ALTO:
            pieza = nueva
        time.sleep(0.2)

    elif keyboard.is_pressed('space'):
        # Colocar pieza y sumar puntos al jugador actual
        colocadas.append((pieza, x, y))
        score.sumar_puntos_por_pieza(jugador_actual, pieza)
        pieza = piezas(6)
        x, y = 0, 0
        
        # Cambiar turno
        if jugador_actual == "Jugador 1":
            jugador_actual = "Jugador 2"
        else:
            jugador_actual = "Jugador 1"
            
        time.sleep(0.3)

    elif keyboard.is_pressed('c'):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Cambiando ficha...")

        def pedir_figura():
            while True:
                try:
                    figura = int(input("Elige una figura (0-9): "))
                    if 0 <= figura <= 9:
                        return figura
                    else:
                        print("Por favor, ingresa un número entre 0 y 9.")
                except ValueError:
                    print("Entrada inválida, por favor ingresa un número.")

        figura_nueva = pedir_figura()
        pieza = piezas(figura_nueva)
        x, y = 0, 0
