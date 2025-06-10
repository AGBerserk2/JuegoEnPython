
# mostrar los puntos de cada jugador
# gregory

class Score:
    def __init__(self):
        self.puntos_por_jugador = {}

    def registrar_jugador(self, jugador_nombre):
        self.puntos_por_jugador[jugador_nombre] = 0

    def sumar_puntos_por_pieza(self, jugador_nombre, piezas):
        puntos = sum(celda == 1 for fila in piezas for celda in fila)
        self.puntos_por_jugador[jugador_nombre] += puntos
        return puntos

    def obtener_puntos(self, jugador_nombre):
        return self.puntos_por_jugador[jugador_nombre]

    def determinar_ganador(self):
        puntos_j1 = self.obtener_puntos("Jugador 1")
        puntos_j2 = self.obtener_puntos("Jugador 2")
        if puntos_j1 > puntos_j2:
            return "Jugador 1"
        elif puntos_j2 > puntos_j1:
            return "Jugador 2"
        else:
            return "Empate"

