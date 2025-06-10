from figuras import piezas, rotar_pieza
import os
import time
import keyboard
from score import Score
import random

class Movimiento:
    def __init__(self):
        self.TABLERO_ALTO = 20
        self.TABLERO_ANCHO = 20
        self.x, self.y = 0, 0
        self.pieza = piezas(random.randint(0,9))
        self.colocadas = []
        self.jugador_actual = "Jugador 1"
        self.score = Score()
        self.score.registrar_jugador("Jugador 1")
        self.score.registrar_jugador("Jugador 2")

    def dibujar_tablero(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        tablero = [['⬜' for _ in range(self.TABLERO_ANCHO)] for _ in range(self.TABLERO_ALTO)]

        for p_colocada, px, py in self.colocadas:
            for i in range(len(p_colocada)):
                for j in range(len(p_colocada[0])):
                    if p_colocada[i][j] == 1:
                        if 0 <= py + i < self.TABLERO_ALTO and 0 <= px + j < self.TABLERO_ANCHO:
                            tablero[py + i][px + j] = '🟩'

        for i in range(len(self.pieza)):
            for j in range(len(self.pieza[0])):
                if self.pieza[i][j] == 1:
                    if 0 <= self.y + i < self.TABLERO_ALTO and 0 <= self.x + j < self.TABLERO_ANCHO:
                        tablero[self.y + i][self.x + j] = '🟦'

        for fila in tablero:
            print(''.join(fila))

        print(f"\nTurno de: {self.jugador_actual}")
        print("Puntaje Jugador 1:", self.score.obtener_puntos("Jugador 1"))
        print("Puntaje Jugador 2:", self.score.obtener_puntos("Jugador 2"))

    def movimiento_tablero(self):
        while True:
            self.dibujar_tablero()
            time.sleep(0.1)

            if keyboard.is_pressed('esc'):
                break
            elif keyboard.is_pressed('left') and self.x > 0:
                self.x -= 1
            elif keyboard.is_pressed('right') and self.x + len(self.pieza[0]) < self.TABLERO_ANCHO:
                self.x += 1
            elif keyboard.is_pressed('up') and self.y > 0:
                self.y -= 1
            elif keyboard.is_pressed('down') and self.y + len(self.pieza) < self.TABLERO_ALTO:
                self.y += 1
            elif keyboard.is_pressed('r'):
                nueva = rotar_pieza(self.pieza)
                if self.x + len(nueva[0]) <= self.TABLERO_ANCHO and self.y + len(nueva) <= self.TABLERO_ALTO:
                    self.pieza = nueva
                time.sleep(0.2)
            elif keyboard.is_pressed('space'):
                self.colocadas.append((self.pieza, self.x, self.y))
                self.score.sumar_puntos_por_pieza(self.jugador_actual, self.pieza)
                self.pieza = piezas(random.randint(0,9))
                self.x, self.y = 0, 0
                self.jugador_actual = "Jugador 2" if self.jugador_actual == "Jugador 1" else "Jugador 1"
                time.sleep(0.3)
            elif keyboard.is_pressed('c'):
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Cambiando ficha...")


                figura_nueva = self.pedir_figura()
                self.pieza = piezas(figura_nueva)
                self.x, self.y = 0, 0

    def pedir_figura(self):
        while True:
            try:
                os.system('cls' if os.name == 'nt' else 'clear')
                figura = int(input("Elige una figura (0-9): "))
                if 0 <= figura <= 9:
                    return figura
                else:
                    print("Por favor, ingresa un número entre 0 y 9.")
            except ValueError:
                print("Entrada inválida, por favor ingresa un número.")
# Ejecutar el juego
juego = Movimiento()
juego.movimiento_tablero()
