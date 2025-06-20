from figuras import piezas, rotar_pieza  
import os  
import time  
import keyboard  
from score import Score  
from logica import Logica  
import random  
  
class Movimiento:  
    def __init__(self, modo_ia=False):  
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
        # Nuevas líneas para IA  
        self.modo_ia = modo_ia  
        if modo_ia:  
            self.piezas_disponibles_ia = [piezas(i) for i in range(10)]  
  
    def dibujar_tablero(self):  
        os.system('cls' if os.name == 'nt' else 'clear')  
        tablero = [['⬜' for _ in range(self.TABLERO_ANCHO)] for _ in range(self.TABLERO_ALTO)]  
  
        for p_colocada, px, py, jugador in self.colocadas:  
            for i in range(len(p_colocada)):  
                for j in range(len(p_colocada[0])):  
                    if p_colocada[i][j] == 1:  
                        if 0 <= py + i < self.TABLERO_ALTO and 0 <= px + j < self.TABLERO_ANCHO:  
                            tablero[py + i][px + j] = '🟩' if jugador == "Jugador 1" else '🟥'  
  
        # Solo mostrar pieza actual si NO es turno de IA  
        if not (self.modo_ia and self.jugador_actual == "Jugador 2"):  
            for i in range(len(self.pieza)):  
                for j in range(len(self.pieza[0])):  
                    if self.pieza[i][j] == 1:  
                        if 0 <= self.y + i < self.TABLERO_ALTO and 0 <= self.x + j < self.TABLERO_ANCHO:  
                            tablero[self.y + i][self.x + j] = '🟦'  
  
        for fila in tablero:  
            print(''.join(fila))  
  
        print(f"\nTurno de: {self.jugador_actual}")  
        if self.modo_ia and self.jugador_actual == "Jugador 2":  
            print("🤖 IA está jugando...")  
        print("Puntaje Jugador 1:", self.score.obtener_puntos("Jugador 1"))  
        print("Puntaje Jugador 2 (IA):" if self.modo_ia else "Puntaje Jugador 2:", self.score.obtener_puntos("Jugador 2"))  
  
    def movimiento_tablero(self):  
        while True:  
            self.dibujar_tablero()  
              
            # NUEVA LÓGICA: Si es turno de IA, ejecutar movimiento automático  
            if self.modo_ia and self.jugador_actual == "Jugador 2":  
                self._ejecutar_turno_ia()  
                continue  
              
            # Código original para jugador humano  
            keyboard.read_event()  
  
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
  
    # NUEVO MÉTODO: Lógica para el turno de la IA  
    def _ejecutar_turno_ia(self):  
        print("🤖 IA está pensando...")  
        time.sleep(1.5)  # Pausa dramática  
          
        mejor_movimiento = self._encontrar_mejor_movimiento_ia()  
          
        if mejor_movimiento:  
            pieza, x, y = mejor_movimiento  
            self.colocadas.append((pieza, x, y, self.jugador_actual))  
            self.score.sumar_puntos_por_pieza(self.jugador_actual, pieza)  
            print(f"🤖 IA colocó pieza en posición ({x}, {y})")  
            self.jugador_actual = "Jugador 1"  
        else:  
            print("🤖 IA no puede hacer más movimientos")  
            self.jugador_actual = "Jugador 1"  
          
        time.sleep(2)  # Mostrar resultado  
  
    # NUEVO MÉTODO: Algoritmo de decisión de la IA  
    def _encontrar_mejor_movimiento_ia(self):  
        mejores_movimientos = []  
          
        # Usar las mismas piezas disponibles que el sistema original  
        for i in range(10):  
            pieza = piezas(i)  
            for rot in range(4):  # Probar 4 rotaciones  
                pieza_rotada = pieza  
                for _ in range(rot):  
                    pieza_rotada = rotar_pieza(pieza_rotada)  
                  
                # Probar todas las posiciones del tablero  
                for y in range(self.TABLERO_ALTO):  
                    for x in range(self.TABLERO_ANCHO):  
                        if self._es_movimiento_valido_ia(pieza_rotada, x, y):  
                            puntos = sum(celda == 1 for fila in pieza_rotada for celda in fila)  
                            mejores_movimientos.append((pieza_rotada, x, y, puntos))  
          
        if mejores_movimientos:  
            # Ordenar por puntos y tomar el mejor  
            mejores_movimientos.sort(key=lambda x: x[3], reverse=True)  
            return mejores_movimientos[0][:3]  # pieza, x, y  
        return None  
  
    # NUEVO MÉTODO: Validación de movimientos para IA  
    def _es_movimiento_valido_ia(self, pieza, x, y):  
        # Usar la misma lógica de validación que el juego original  
        if not self.logica.es_posicion_valida(pieza, x, y, self.colocadas):  
            return False  
        if self.logica.es_contacto_lateral(pieza, x, y, self.colocadas, self.jugador_actual):  
            return False  
          
        piezas_jugador = self.logica.filtrar_colocadas_por_jugador(self.colocadas, self.jugador_actual)  
        turno = len(piezas_jugador)  
          
        if turno == 0:  
            return self.logica.es_primera_colocacion_valida(pieza, x, y, self.jugador_actual)  
        else:  
            return self.logica.es_adyacente_diagonal(pieza, x, y, self.colocadas, self.jugador_actual)  
  
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