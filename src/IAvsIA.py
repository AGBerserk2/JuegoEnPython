from figuras import piezas  
from score import Score  
from logica import Logica  
from IA import IA  
import os  
import time  
import random  
  
class JuegoIA:  
    def __init__(self):  
        self.TABLERO_ALTO = 10  
        self.TABLERO_ANCHO = 10  
        self.colocadas = []  
        self.score = Score()  
        self.score.registrar_jugador("Jugador 1")  
        self.score.registrar_jugador("Jugador 2")  
        self.logica = Logica(self.TABLERO_ANCHO, self.TABLERO_ALTO)  
          
        # Crear las dos IAs  
        self.ia1 = IA("Jugador 1", self.logica)  
        self.ia2 = IA("Jugador 2", self.logica)  
        self.jugador_actual = "Jugador 1"  
  
    def dibujar_tablero(self):  
        os.system('cls' if os.name == 'nt' else 'clear')  
        tablero = [['⬜' for _ in range(self.TABLERO_ANCHO)] for _ in range(self.TABLERO_ALTO)]  
  
        for p_colocada, px, py, jugador in self.colocadas:  
            for i in range(len(p_colocada)):  
                for j in range(len(p_colocada[0])):  
                    if p_colocada[i][j] == 1:  
                        if 0 <= py + i < self.TABLERO_ALTO and 0 <= px + j < self.TABLERO_ANCHO:  
                            tablero[py + i][px + j] = '🟩' if jugador == "Jugador 1" else '🟥'  
  
        for fila in tablero:  
            print(''.join(fila))  
  
        print(f"\nTurno de: {self.jugador_actual}")  
        print("Puntaje Heimer:", self.score.obtener_puntos("Jugador 1"))  
        print("Puntaje Minimax++:", self.score.obtener_puntos("Jugador 2"))  
  
    def jugar_automatico(self):  
        turnos_sin_movimiento = 0  
        max_turnos = 100  # Límite de seguridad  
        turno_actual = 0  
          
        while turno_actual < max_turnos and turnos_sin_movimiento < 2:  
            self.dibujar_tablero()  
            time.sleep(1)  # Pausa para ver el progreso  
              
            # Seleccionar IA actual  
            ia_actual = self.ia1 if self.jugador_actual == "Jugador 1" else self.ia2  
              
            # IA hace su movimiento  
            movimiento = ia_actual.minimax(self.colocadas)  
              
            if movimiento:  
                pieza, x, y = movimiento  
                self.colocadas.append((pieza, x, y, self.jugador_actual))  
                self.score.sumar_puntos_por_pieza(self.jugador_actual, pieza)  
                  
                # Remover pieza usada de las disponibles  
                if pieza in ia_actual.piezas_disponibles:  
                    ia_actual.piezas_disponibles.remove(pieza)  
                  
                print(f"{self.jugador_actual} colocó una pieza en ({x}, {y})")  
                turnos_sin_movimiento = 0  
            else:  
                print(f"{self.jugador_actual} no puede hacer movimientos")  
                turnos_sin_movimiento += 1  
              
            # Cambiar turno  
            self.jugador_actual = "Jugador 2" if self.jugador_actual == "Jugador 1" else "Jugador 1"  
            turno_actual += 1  
            time.sleep(2)  
          
        # Mostrar resultado final  
        self.mostrar_resultado_final()  
        time.sleep(5)  
  
    def mostrar_resultado_final(self):  
        self.dibujar_tablero()  
        print("\n=== JUEGO TERMINADO ===")  
        ganador = self.score.determinar_ganador()  
        if ganador == "Empate":  
            print("¡Es un empate!")  
        else:  
            print(f"¡{ganador} es el ganador!")  
          
        input("Presiona Enter para continuar...")
