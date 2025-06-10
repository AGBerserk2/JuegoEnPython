# Verificar si el movimiento es valido y si el usuario puede moverse
# kelvin, angel

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
