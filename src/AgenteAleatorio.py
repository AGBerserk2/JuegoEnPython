import random
from figuras import rotar_pieza
from copy import deepcopy

class AgenteAleatorio:
    def __init__(self, jugador, logica, piezas_disponibles):
        self.jugador = jugador
        self.logica = logica
        self.piezas_disponibles = piezas_disponibles

    def encontrar_mejor_jugada(self, colocadas, fichas_usadas):
        movimientos_posibles = []

        for i in range(10):
            if fichas_usadas[i] >= 2:
                continue
            pieza = self.piezas_disponibles[i]
            for rot in range(4):
                pieza_rotada = pieza
                for _ in range(rot):
                    pieza_rotada = rotar_pieza(pieza_rotada)
                for y in range(self.logica.alto):
                    for x in range(self.logica.ancho):
                        if self.logica.es_posicion_valida(pieza_rotada, x, y, colocadas) and \
                           not self.logica.es_contacto_lateral(pieza_rotada, x, y, colocadas, self.jugador):
                            piezas_jugador = self.logica.filtrar_colocadas_por_jugador(colocadas, self.jugador)
                            turno = len(piezas_jugador)
                            if (turno == 0 and self.logica.es_primera_colocacion_valida(pieza_rotada, x, y, self.jugador)) or \
                               (turno > 0 and self.logica.es_adyacente_diagonal(pieza_rotada, x, y, colocadas, self.jugador)):
                                movimientos_posibles.append((pieza_rotada, x, y, i))

        return random.choice(movimientos_posibles)[:3] if movimientos_posibles else None


