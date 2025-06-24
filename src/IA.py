from figuras import piezas, rotar_pieza
import random
import copy

class IA:
    def __init__(self, logica, jugador="Jugador 2"):
        self.logica = logica
        self.jugador = jugador
        self.piezas_disponibles = [piezas(i) for i in range(10)]

    def encontrar_mejor_movimiento(self, colocadas):
        mejor_valor = float("-inf")
        mejor_movimiento = None

        for pieza in self.piezas_disponibles:
            for rot in range(4):
                pieza_rotada = pieza
                for _ in range(rot):
                    pieza_rotada = rotar_pieza(pieza_rotada)

                for y in range(self.logica.alto):
                    for x in range(self.logica.ancho):
                        if self._es_movimiento_valido(pieza_rotada, x, y, colocadas):
                            nuevo_estado = copy.deepcopy(colocadas)
                            nuevo_estado.append((pieza_rotada, x, y, self.jugador))
                            valor = self.minimax(nuevo_estado, profundidad=2, es_max=False, alfa=float("-inf"), beta=float("inf"))
                            if valor > mejor_valor:
                                mejor_valor = valor
                                mejor_movimiento = (pieza_rotada, x, y)

        return mejor_movimiento

    def minimax(self, colocadas, profundidad, es_max, alfa, beta):
        if profundidad == 0 or self.logica.juego_terminado(colocadas, "Jugador 1", "Jugador 2", 10):
            return self.evaluar_estado(colocadas)

        jugador_actual = self.jugador if es_max else "Jugador 1"
        mejor_valor = float("-inf") if es_max else float("inf")

        piezas_restantes = [piezas(i) for i in range(10)]
        colocadas_por_jugador = self.logica.filtrar_colocadas_por_jugador(colocadas, jugador_actual)
        for colocada in colocadas_por_jugador:
            for pieza in piezas_restantes:
                if pieza in colocadas:
                    continue  # Ya usada

        for pieza in piezas_restantes:
            for rot in range(4):
                pieza_rotada = pieza
                for _ in range(rot):
                    pieza_rotada = rotar_pieza(pieza_rotada)

                for y in range(self.logica.alto):
                    for x in range(self.logica.ancho):
                        if self._es_movimiento_valido(pieza_rotada, x, y, colocadas, jugador_actual):
                            nuevo_estado = copy.deepcopy(colocadas)
                            nuevo_estado.append((pieza_rotada, x, y, jugador_actual))
                            valor = self.minimax(nuevo_estado, profundidad - 1, not es_max, alfa, beta)

                            if es_max:
                                mejor_valor = max(mejor_valor, valor)
                                alfa = max(alfa, valor)
                            else:
                                mejor_valor = min(mejor_valor, valor)
                                beta = min(beta, valor)

                            if beta <= alfa:
                                return mejor_valor

        return mejor_valor

    def evaluar_estado(self, colocadas):
        piezas_jugador = self.logica.filtrar_colocadas_por_jugador(colocadas, self.jugador)

        # Heurística 1: Casillas ocupadas
        casillas = sum(cell == 1 for pieza, _, _, _ in piezas_jugador for fila in pieza for cell in fila)

        # Heurística 2: Penalización por piezas no colocadas (premiamos usar piezas)
        piezas_colocadas = len(piezas_jugador)
        piezas_restantes = 10 - piezas_colocadas
        penalizacion = piezas_restantes * 2

        # Heurística 3: Control del centro
        centro_x, centro_y = self.logica.ancho // 2, self.logica.alto // 2
        control_centro = 0
        for pieza, x, y, _ in piezas_jugador:
            for i in range(len(pieza)):
                for j in range(len(pieza[0])):
                    if pieza[i][j] == 1:
                        dx = abs((x + j) - centro_x)
                        dy = abs((y + i) - centro_y)
                        control_centro += max(0, 5 - (dx + dy))  # más cerca del centro = mejor

        # Heurística 4: Número de posibles movimientos futuros
        posibles_movs = 0
        for pieza in self.piezas_disponibles:
            for rot in range(4):
                pieza_rotada = pieza
                for _ in range(rot):
                    pieza_rotada = rotar_pieza(pieza_rotada)
                for y in range(self.logica.alto):
                    for x in range(self.logica.ancho):
                        if self._es_movimiento_valido(pieza_rotada, x, y, colocadas):
                            posibles_movs += 1

        # Heurística 5: Penalización por estar bloqueado (contacto lateral)
        penalizacion_contacto = 0
        for pieza, x, y, _ in piezas_jugador:
            if self.logica.es_contacto_lateral(pieza, x, y, colocadas, self.jugador):
                penalizacion_contacto += 5

        return casillas + control_centro + posibles_movs - penalizacion - penalizacion_contacto

    def _es_movimiento_valido(self, pieza, x, y, colocadas, jugador=None):
        if jugador is None:
            jugador = self.jugador
        if not self.logica.es_posicion_valida(pieza, x, y, colocadas):
            return False
        if self.logica.es_contacto_lateral(pieza, x, y, colocadas, jugador):
            return False

        piezas_jugador = self.logica.filtrar_colocadas_por_jugador(colocadas, jugador)
        turno = len(piezas_jugador)

        if turno == 0:
            return self.logica.es_primera_colocacion_valida(pieza, x, y, jugador)
        else:
            return self.logica.es_adyacente_diagonal(pieza, x, y, colocadas, jugador)
