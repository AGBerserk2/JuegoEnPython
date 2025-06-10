# Verificar si el movimiento es valido y si el usuario puede moverse
# kelvin, angel
<<<<<<< HEAD
# logica.py
from typing import List, Dict
from figuras import rotar_pieza
from score import Score

# Mapa de colores por jugador
colores_por_jugador = {
    "Kelvin": {"code": 1, "symbol": "🟥"},  # Rojo para Kelvin
    "Ana": {"code": 2, "symbol": "🟦"}      # Azul para Ana
}

# Celda vacía
EMPTY_CELL = "⬜"

def es_movimiento_valido(tablero: List[List[int]], pieza: List[List[int]], fila_inicio: int, col_inicio: int, jugador: str, es_primer_movimiento: Dict[str, bool]) -> bool:
    """
    Valida un movimiento según las reglas de Blokus:
    - Dentro de los límites.
    - Sin superposición.
    - Toque de esquina con pieza del mismo jugador.
    - Sin bordes compartidos con piezas del mismo jugador.
    - Primer movimiento en esquina específica.
    """
    filas_tablero = len(tablero)
    cols_tablero = len(tablero[0])
    filas_pieza = len(pieza)
    cols_pieza = len(pieza[0])
    color = colores_por_jugador[jugador]["code"]

    # Verificar límites y superposición
    for i in range(filas_pieza):
        for j in range(cols_pieza):
            if pieza[i][j] == 1:
                fila_tablero = fila_inicio + i
                col_tablero = col_inicio + j
                if (fila_tablero >= filas_tablero or col_tablero >= cols_tablero or
                        fila_tablero < 0 or col_tablero < 0):
                    return False
                if tablero[fila_tablero][col_tablero] != 0:
                    return False

    # Verificar primer movimiento
    if es_primer_movimiento.get(jugador, True):
        start_corners = {
            "Kelvin": (0, 0),
            "Ana": (19, 19)
        }
        start_fila, start_col = start_corners[jugador]
        corner_covered = False
        for i in range(filas_pieza):
            for j in range(cols_pieza):
                if pieza[i][j] == 1 and (fila_inicio + i == start_fila and col_inicio + j == start_col):
                    corner_covered = True
                    break
        if not corner_covered:
            return False

    # Verificar toque de esquinas y no bordes compartidos
    corners_touching = False
    for i in range(filas_pieza):
        for j in range(cols_pieza):
            if pieza[i][j] == 1:
                fila_tablero = fila_inicio + i
                col_tablero = col_inicio + j

                # Bordes: no piezas del mismo jugador
                for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    ni, nj = fila_tablero + di, col_tablero + dj
                    if (0 <= ni < filas_tablero and 0 <= nj < cols_tablero and
                            tablero[ni][nj] == color):
                        return False

                # Esquinas: al menos una pieza del mismo jugador
                for di, dj in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    ni, nj = fila_tablero + di, col_tablero + dj
                    if (0 <= ni < filas_tablero and 0 <= nj < cols_tablero and
                            tablero[ni][nj] == color):
                        corners_touching = True

    if not es_primer_movimiento.get(jugador, True) and not corners_touching:
        return False

    return True

def colocar_pieza(tablero: List[List[int]], pieza: List[List[int]], fila_inicio: int, col_inicio: int, color: int) -> None:
    """
    Coloca una pieza en el tablero.
    """
    for i in range(len(pieza)):
        for j in range(len(pieza[0])):
            if pieza[i][j] == 1:
                tablero[fila_inicio + i][col_inicio + j] = color

def determinar_ganador(score: Score) -> str:
    """
    Determina el ganador según los puntos.
    """
    max_puntos = max(score.puntos_por_jugador.values())
    ganadores = [jugador for jugador, puntos in score.puntos_por_jugador.items() if puntos == max_puntos]
    if len(ganadores) == 1:
        return f"El ganador es {ganadores[0]} con {max_puntos} puntos."
    return f"Empate entre: {', '.join(ganadores)} con {max_puntos} puntos."

def mostrar_resultado(score: Score) -> None:
    """
    Muestra los puntajes finales.
    """
    print("Resultado Final:")
    for jugador, puntos in score.puntos_por_jugador.items():
        print(f"{jugador}: {puntos} puntos")

def mostrar_tablero(tablero: List[List[int]]) -> None:
    """
    Muestra el tablero con colores por jugador.
    """
    color_map = {0: EMPTY_CELL}
    for jugador, info in colores_por_jugador.items():
        color_map[info["code"]] = info["symbol"]

    for fila in tablero:
        print(''.join(color_map.get(celda, EMPTY_CELL) for celda in fila))
from typing import List, Dict
from figuras import rotar_pieza
from score import Score

# Mapa de colores por jugador
colores_por_jugador = {
    "Kelvin": {"code": 1, "symbol": "🟥"},  # Rojo para Kelvin
    "Ana": {"code": 2, "symbol": "🟦"}      # Azul para Ana
}

# Celda vacía
EMPTY_CELL = "⬜"

def es_movimiento_valido(tablero: List[List[int]], pieza: List[List[int]], fila_inicio: int, col_inicio: int, jugador: str, es_primer_movimiento: Dict[str, bool]) -> bool:
    """
    Valida un movimiento según las reglas de Blokus:
    - Dentro de los límites.
    - Sin superposición.
    - Toque de esquina con pieza del mismo jugador.
    - Sin bordes compartidos con piezas del mismo jugador.
    - Primer movimiento en esquina específica.
    """
    filas_tablero = len(tablero)
    cols_tablero = len(tablero[0])
    filas_pieza = len(pieza)
    cols_pieza = len(pieza[0])
    color = colores_por_jugador[jugador]["code"]

    # Verificar límites y superposición
    for i in range(filas_pieza):
        for j in range(cols_pieza):
            if pieza[i][j] == 1:
                fila_tablero = fila_inicio + i
                col_tablero = col_inicio + j
                if (fila_tablero >= filas_tablero or col_tablero >= cols_tablero or
                        fila_tablero < 0 or col_tablero < 0):
                    return False
                if tablero[fila_tablero][col_tablero] != 0:
                    return False

    # Verificar primer movimiento
    if es_primer_movimiento.get(jugador, True):
        start_corners = {
            "Kelvin": (0, 0),
            "Ana": (19, 19)
        }
        start_fila, start_col = start_corners[jugador]
        corner_covered = False
        for i in range(filas_pieza):
            for j in range(cols_pieza):
                if pieza[i][j] == 1 and (fila_inicio + i == start_fila and col_inicio + j == start_col):
                    corner_covered = True
                    break
        if not corner_covered:
            return False

    # Verificar toque de esquinas y no bordes compartidos
    corners_touching = False
    for i in range(filas_pieza):
        for j in range(cols_pieza):
            if pieza[i][j] == 1:
                fila_tablero = fila_inicio + i
                col_tablero = col_inicio + j

                # Bordes: no piezas del mismo jugador
                for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    ni, nj = fila_tablero + di, col_tablero + dj
                    if (0 <= ni < filas_tablero and 0 <= nj < cols_tablero and
                            tablero[ni][nj] == color):
                        return False

                # Esquinas: al menos una pieza del mismo jugador
                for di, dj in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    ni, nj = fila_tablero + di, col_tablero + dj
                    if (0 <= ni < filas_tablero and 0 <= nj < cols_tablero and
                            tablero[ni][nj] == color):
                        corners_touching = True

    if not es_primer_movimiento.get(jugador, True) and not corners_touching:
        return False

    return True

def colocar_pieza(tablero: List[List[int]], pieza: List[List[int]], fila_inicio: int, col_inicio: int, color: int) -> None:
    """
    Coloca una pieza en el tablero.
    """
    for i in range(len(pieza)):
        for j in range(len(pieza[0])):
            if pieza[i][j] == 1:
                tablero[fila_inicio + i][col_inicio + j] = color

def determinar_ganador(score: Score) -> str:
    """
    Determina el ganador según los puntos.
    """
    max_puntos = max(score.puntos_por_jugador.values())
    ganadores = [jugador for jugador, puntos in score.puntos_por_jugador.items() if puntos == max_puntos]
    if len(ganadores) == 1:
        return f"El ganador es {ganadores[0]} con {max_puntos} puntos."
    return f"Empate entre: {', '.join(ganadores)} con {max_puntos} puntos."

def mostrar_resultado(score: Score) -> None:
    """
    Muestra los puntajes finales.
    """
    print("Resultado Final:")
    for jugador, puntos in score.puntos_por_jugador.items():
        print(f"{jugador}: {puntos} puntos")

def mostrar_tablero(tablero: List[List[int]]) -> None:
    """
    Muestra el tablero con colores por jugador.
    """
    color_map = {0: EMPTY_CELL}
    for jugador, info in colores_por_jugador.items():
        color_map[info["code"]] = info["symbol"]

    for fila in tablero:
        print(''.join(color_map.get(celda, EMPTY_CELL) for celda in fila))




=======

class Logica:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto

    def es_posicion_valida(self, pieza, x, y, colocadas):
        for i in range(len(pieza)):
            for j in range(len(pieza[0])):
                if pieza[i][j] == 1:
                    tx, ty = x + j, y + i
                    if not (0 <= tx < self.ancho and 0 <= ty < self.alto):
                        return False
                    for otra, px, py, _ in colocadas:
                        for ii in range(len(otra)):
                            for jj in range(len(otra[0])):
                                if otra[ii][jj] == 1 and tx == px + jj and ty == py + ii:
                                    return False
        return True

    def es_adyacente_diagonal(self, pieza, x, y, colocadas, jugador):
        colocadas_jugador = self.filtrar_colocadas_por_jugador(colocadas, jugador)
        for i in range(len(pieza)):
            for j in range(len(pieza[0])):
                if pieza[i][j] == 1:
                    px, py = x + j, y + i
                    diagonales = [(px-1, py-1), (px+1, py-1), (px-1, py+1), (px+1, py+1)]
                    for ox, oy in diagonales:
                        for otra, cx, cy in colocadas_jugador:
                            for ii in range(len(otra)):
                                for jj in range(len(otra[0])):
                                    if otra[ii][jj] == 1 and ox == cx + jj and oy == cy + ii:
                                        return True
        return False if colocadas_jugador else True  # primera pieza puede ir sin adyacencia

    def es_contacto_lateral(self, pieza, x, y, colocadas, jugador):
        colocadas_jugador = self.filtrar_colocadas_por_jugador(colocadas, jugador)
        for i in range(len(pieza)):
            for j in range(len(pieza[0])):
                if pieza[i][j] == 1:
                    px, py = x + j, y + i
                    laterales = [(px-1, py), (px+1, py), (px, py-1), (px, py+1)]
                    for ox, oy in laterales:
                        for otra, cx, cy in colocadas_jugador:
                            for ii in range(len(otra)):
                                for jj in range(len(otra[0])):
                                    if otra[ii][jj] == 1 and ox == cx + jj and oy == cy + ii:
                                        return True
        return False

    def es_primera_colocacion_valida(self, pieza, x, y, jugador):
        esquina = (0, 0) if jugador == "Jugador 1" else (self.ancho - 1, self.alto - 1)
        for i in range(len(pieza)):
            for j in range(len(pieza[0])):
                if pieza[i][j] == 1:
                    px, py = x + j, y + i
                    if (px, py) == esquina:
                        return True
        return False

    def filtrar_colocadas_por_jugador(self, colocadas, jugador):
        return [(pieza, x, y) for pieza, x, y, j in colocadas if j == jugador]
>>>>>>> 32d86c9c7fd78f902c072e8db0f2fff5249630ea
