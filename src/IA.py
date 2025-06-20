from figuras import piezas, rotar_pieza  
import random  
  
class IA:  
    def __init__(self, logica, jugador="Jugador 2"):  
        self.logica = logica  
        self.jugador = jugador  
        self.piezas_disponibles = [piezas(i) for i in range(10)]  
      
    def encontrar_mejor_movimiento(self, colocadas):  
        mejores_movimientos = []  
          
        for pieza in self.piezas_disponibles:  
            for rot in range(4):  
                pieza_rotada = pieza  
                for _ in range(rot):  
                    pieza_rotada = rotar_pieza(pieza_rotada)  
                  
                for y in range(self.logica.alto):  
                    for x in range(self.logica.ancho):  
                        if self._es_movimiento_valido(pieza_rotada, x, y, colocadas):  
                            puntos = sum(celda == 1 for fila in pieza_rotada for celda in fila)  
                            mejores_movimientos.append((pieza_rotada, x, y, puntos))  
          
        if mejores_movimientos:  
            # Ordenar por puntos y tomar el mejor  
            mejores_movimientos.sort(key=lambda x: x[3], reverse=True)  
            return mejores_movimientos[0][:3]  # pieza, x, y  
        return None  
      
    def _es_movimiento_valido(self, pieza, x, y, colocadas):  
        if not self.logica.es_posicion_valida(pieza, x, y, colocadas):  
            return False  
        if self.logica.es_contacto_lateral(pieza, x, y, colocadas, self.jugador):  
            return False  
          
        piezas_jugador = self.logica.filtrar_colocadas_por_jugador(colocadas, self.jugador)  
        turno = len(piezas_jugador)  
          
        if turno == 0:  
            return self.logica.es_primera_colocacion_valida(pieza, x, y, self.jugador)  
        else:  
            return self.logica.es_adyacente_diagonal(pieza, x, y, colocadas, self.jugador)