
import time
from copy import deepcopy
from figuras import rotar_pieza

class AgenteMinimax:
    def __init__(self, jugador, logica, piezas_disponibles, tiempo_limite=3):
        self.jugador = jugador
        self.logica = logica
        self.piezas_disponibles = piezas_disponibles
        self.tiempo_limite = tiempo_limite
        self.inicio_tiempo = None

    def encontrar_mejor_jugada(self, colocadas, fichas_usadas):
        self.inicio_tiempo = time.time()
        mejor_valor = float('-inf')
        mejor_mov = None

        piezas_ordenadas = sorted(
            [(i, self.piezas_disponibles[i]) for i in range(10)],
            key=lambda x: -sum(cell == 1 for fila in x[1] for cell in fila)
        )

        for i, pieza_base in piezas_ordenadas:
            if fichas_usadas[i] >= 2:
                continue
            for rot in range(4):
                pieza_rotada = pieza_base
                for _ in range(rot):
                    pieza_rotada = rotar_pieza(pieza_rotada)

                for y in range(self.logica.alto):
                    for x in range(self.logica.ancho):
                        if self._es_movimiento_valido(pieza_rotada, x, y, colocadas):
                            nueva_colocadas = deepcopy(colocadas)
                            nueva_colocadas.append((pieza_rotada, x, y, self.jugador))
                            nuevas_fichas_usadas = deepcopy(fichas_usadas)
                            nuevas_fichas_usadas[i] += 1

                            if self._tiempo_agotado():
                                return mejor_mov

                            valor = self.minimax(
                                nueva_colocadas,
                                profundidad=2,
                                alpha=float('-inf'),
                                beta=float('inf'),
                                maximizando=False,
                                fichas_usadas=nuevas_fichas_usadas
                            )

                            if valor > mejor_valor:
                                mejor_valor = valor
                                mejor_mov = (pieza_rotada, x, y)

        return mejor_mov

    def minimax(self, estado, profundidad, alpha, beta, maximizando, fichas_usadas):
        if profundidad == 0 or self._tiempo_agotado():
            return self.evaluar_estado(estado)

        jugador_actual = self.jugador if maximizando else (
            "Jugador 2" if self.jugador == "Jugador 1" else "Jugador 1"
        )

        if maximizando:
            max_eval = float('-inf')
            for mov, ficha_id in self._generar_movimientos(estado, jugador_actual, fichas_usadas):
                nuevo_estado = deepcopy(estado)
                nuevo_estado.append((mov[0], mov[1], mov[2], jugador_actual))
                nuevas_fichas_usadas = deepcopy(fichas_usadas)
                nuevas_fichas_usadas[ficha_id] += 1

                if self._tiempo_agotado():
                    break

                eval = self.minimax(nuevo_estado, profundidad - 1, alpha, beta, False, nuevas_fichas_usadas)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for mov, ficha_id in self._generar_movimientos(estado, jugador_actual, fichas_usadas):
                nuevo_estado = deepcopy(estado)
                nuevo_estado.append((mov[0], mov[1], mov[2], jugador_actual))
                nuevas_fichas_usadas = deepcopy(fichas_usadas)
                nuevas_fichas_usadas[ficha_id] += 1

                if self._tiempo_agotado():
                    break

                eval = self.minimax(nuevo_estado, profundidad - 1, alpha, beta, True, nuevas_fichas_usadas)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def _generar_movimientos(self, colocadas, jugador, fichas_usadas):
        movimientos = []
        piezas_ordenadas = sorted(
            [(i, self.piezas_disponibles[i]) for i in range(10)],
            key=lambda x: -sum(cell == 1 for fila in x[1] for cell in fila)
        )

        for i, pieza_base in piezas_ordenadas:
            if fichas_usadas[i] >= 2:
                continue
            for rot in range(4):
                pieza_rotada = pieza_base
                for _ in range(rot):
                    pieza_rotada = rotar_pieza(pieza_rotada)
                for y in range(self.logica.alto):
                    for x in range(self.logica.ancho):
                        if self._es_movimiento_valido(pieza_rotada, x, y, colocadas, jugador):
                            movimientos.append(((pieza_rotada, x, y), i))
        return movimientos

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

    def evaluar_estado(self, colocadas):
        piezas_jugador = self.logica.filtrar_colocadas_por_jugador(colocadas, self.jugador)

        # Heurística 1: casillas ocupadas
        casillas = sum(cell == 1 for pieza, x, y, _ in piezas_jugador for fila in pieza for cell in fila)

        # Heurística 2: piezas grandes
        tamaño_total = sum(
            sum(cell == 1 for fila in pieza for cell in fila)
            for pieza, x, y, _ in piezas_jugador
        )

        # Heurística 3: jugabilidad futura
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

        # Heurística 4: penalización por contacto lateral
        penalizacion_contacto = 0
        for pieza, x, y, _ in piezas_jugador:
            if self.logica.es_contacto_lateral(pieza, x, y, colocadas, self.jugador):
                penalizacion_contacto += 5

        # Heurística 5: esquinas abiertas
        esquinas_libres = 0
        ocupadas = {(x + j, y + i)
                    for pieza, x, y, _ in colocadas
                    for i in range(len(pieza))
                    for j in range(len(pieza[0]))
                    if pieza[i][j] == 1}

        for pieza, x, y, _ in piezas_jugador:
            for i in range(len(pieza)):
                for j in range(len(pieza[0])):
                    if pieza[i][j] == 1:
                        cx, cy = x + j, y + i
                        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                            nx, ny = cx + dx, cy + dy
                            if 0 <= nx < self.logica.ancho and 0 <= ny < self.logica.alto:
                                if (nx, ny) not in ocupadas:
                                    esquinas_libres += 1

        return (
            casillas
            + tamaño_total * 1.5
            + posibles_movs * 0.8
            + esquinas_libres * 0.6
            - penalizacion_contacto
        )

    def _tiempo_agotado(self):
        return (time.time() - self.inicio_tiempo) > self.tiempo_limite


