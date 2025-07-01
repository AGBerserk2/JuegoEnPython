from figuras import piezas, rotar_pieza
import random
import copy
  
class IA:  
    def __init__(self, jugador_nombre, logica):  
        self.jugador_nombre = jugador_nombre  
        self.logica = logica  
        self.piezas_disponibles = [piezas(i) for i in range(10)]  
  
    def evaluar_estados(self, colocadas):  
        # Evalúa el estado actual del tablero  
        puntos_propios = len([p for p in colocadas if p[3] == self.jugador_nombre])  
        puntos_oponente = len([p for p in colocadas if p[3] != self.jugador_nombre])  
        return puntos_propios - puntos_oponente  
  
    def movimiento_validos(self, colocadas):  
        # Genera todos los movimientos válidos posibles  
        movimientos = []  
        for pieza in self.piezas_disponibles:  
            for rot in range(4):  
                pieza_rotada = pieza  
                for _ in range(rot):  
                    pieza_rotada = rotar_pieza(pieza_rotada)  
                  
                for y in range(self.logica.alto):  
                    for x in range(self.logica.ancho):  
                        if self._es_movimiento_valido(pieza_rotada, x, y, colocadas):  
                            movimientos.append((pieza_rotada, x, y))  
        return movimientos  
  
    def _es_movimiento_valido(self, pieza, x, y, colocadas):  
        # Usa la lógica existente para validar movimientos  
        if not self.logica.es_posicion_valida(pieza, x, y, colocadas):  
            return False  
        if self.logica.es_contacto_lateral(pieza, x, y, colocadas, self.jugador_nombre):  
            return False  
          
        piezas_jugador = self.logica.filtrar_colocadas_por_jugador(colocadas, self.jugador_nombre)  
        turno = len(piezas_jugador)  
          
        if turno == 0:  
            return self.logica.es_primera_colocacion_valida(pieza, x, y, self.jugador_nombre)  
        else:  
            return self.logica.es_adyacente_diagonal(pieza, x, y, colocadas, self.jugador_nombre)  
  
    def minimax(self, colocadas, profundidad=2):  
        # Implementación simple de minimax  
        movimientos = self.movimiento_validos(colocadas)  
        if not movimientos:  
            return None  
          
        mejor_movimiento = None  
        mejor_puntuacion = float('-inf')  
          
        for movimiento in movimientos:  
            pieza, x, y = movimiento  
            # Simula el movimiento  
            nueva_colocadas = colocadas + [(pieza, x, y, self.jugador_nombre)]  
            puntuacion = self.evaluar_estados(nueva_colocadas)  
              
            if puntuacion > mejor_puntuacion:  
                mejor_puntuacion = puntuacion  
                mejor_movimiento = movimiento  
          
        return mejor_movimiento