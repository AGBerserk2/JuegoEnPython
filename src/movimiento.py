# El movimiento debe ser mediante las flechas del teclado y para confirmar si 
# queremos colocar la figura en esa pocision usamos enter
# jose

from figuras import piezas
from figuras import rotar_pieza
import os
import time
import keyboard



TABLERO_ALTO = 20
TABLERO_ANCHO = 20

x, y = 0, 0
pieza = piezas(5)
colocadas = []

def dibujar_tablero(x, y, pieza, colocadas):
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

while True:
    dibujar_tablero(x, y, pieza, colocadas)
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
        colocadas.append((pieza, x, y))
        pieza = piezas(6)
        x, y = 0, 0
        time.sleep(0.2)

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
