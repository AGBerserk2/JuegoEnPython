from figuras import piezas, rotar_pieza
import os
import time
import keyboard
from score import Score
from logica import Logica
import random

<<<<<<< HEAD

TABLERO_ALTO = 20
TABLERO_ANCHO = 20

class Score:
=======
class Movimiento:
>>>>>>> 32d86c9c7fd78f902c072e8db0f2fff5249630ea
    def __init__(self):
        self.TABLERO_ALTO = 15
        self.TABLERO_ANCHO = 20
        self.x, self.y = 0, 0
        self.pieza = piezas(random.randint(0,9))
        self.colocadas = []
        self.jugador_actual = "Jugador 1"
        self.score = Score()
        self.score.registrar_jugador("Jugador 1")
        self.score.registrar_jugador("Jugador 2")
        self.logica = Logica(self.TABLERO_ANCHO, self.TABLERO_ALTO)

    def dibujar_tablero(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        tablero = [['⬜' for _ in range(self.TABLERO_ANCHO)] for _ in range(self.TABLERO_ALTO)]

        for p_colocada, px, py, jugador in self.colocadas:
            for i in range(len(p_colocada)):
                for j in range(len(p_colocada[0])):
                    if p_colocada[i][j] == 1:
                        if 0 <= py + i < self.TABLERO_ALTO and 0 <= px + j < self.TABLERO_ANCHO:
                            tablero[py + i][px + j] = '🟩' if jugador == "Jugador 1" else '🟥'

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
                piezas_jugador = self.logica.filtrar_colocadas_por_jugador(self.colocadas, self.jugador_actual)
                turno = len(piezas_jugador)

                if not self.logica.es_posicion_valida(self.pieza, self.x, self.y, self.colocadas):
                    print("Posición inválida: la pieza se superpone o está fuera del tablero.")
                    time.sleep(1)
                    continue

                if self.logica.es_contacto_lateral(self.pieza, self.x, self.y,self.colocadas,self.jugador_actual):
                    print("No se permite contacto lateral con tus propias piezas.")
                    time.sleep(1)
                    continue

                if turno == 0:
                    if not self.logica.es_primera_colocacion_valida(self.pieza, self.x, self.y, self.jugador_actual):
                        print("La primera pieza debe tocar la esquina inicial.")
                        time.sleep(1)
                        continue
                else:
                    if not self.logica.es_adyacente_diagonal(self.pieza, self.x, self.y,self.colocadas ,self.jugador_actual):
                        print("Debes colocar la pieza en contacto diagonal con una tuya.")
                        time.sleep(1)
                        continue

                # Colocar pieza
                self.colocadas.append((self.pieza, self.x, self.y, self.jugador_actual))
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
if __name__ == "__main__":
    juego = Movimiento()
    juego.movimiento_tablero()