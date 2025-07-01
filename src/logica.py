# Verificar si el movimiento es valido y si el usuario puede moverse
# kelvin, angel
# logica.py
from figuras import piezas
from figuras import rotar_pieza

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
                        for otra, cx, cy, _ in colocadas_jugador:
                            for ii in range(len(otra)):
                                for jj in range(len(otra[0])):
                                    if otra[ii][jj] == 1 and ox == cx + jj and oy == cy + ii:
                                        return True
        return False if colocadas_jugador else True

    def es_contacto_lateral(self, pieza, x, y, colocadas, jugador):
        colocadas_jugador = self.filtrar_colocadas_por_jugador(colocadas, jugador)
        for i in range(len(pieza)):
            for j in range(len(pieza[0])):
                if pieza[i][j] == 1:
                    px, py = x + j, y + i
                    laterales = [(px-1, py), (px+1, py), (px, py-1), (px, py+1)]
                    for ox, oy in laterales:
                        for otra, cx, cy, _ in colocadas_jugador:
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
        return [(pieza, x, y,j) for pieza, x, y, j in colocadas if j == jugador]

    def puede_jugar(self, piezas_disponibles, colocadas, jugador):
        for pieza in piezas_disponibles:
            for rot in range(4):  # Probar las 4 rotaciones
                pieza_rotada = pieza
                for _ in range(rot):
                    pieza_rotada = rotar_pieza(pieza_rotada)
                for y in range(self.alto):
                    for x in range(self.ancho):
                        if self.es_posicion_valida(pieza_rotada, x, y, colocadas):
                            if not self.es_contacto_lateral(pieza_rotada, x, y, colocadas, jugador):
                                piezas_jugador = self.filtrar_colocadas_por_jugador(colocadas, jugador)
                                turno = len(piezas_jugador)
                                if turno == 0:
                                    if self.es_primera_colocacion_valida(pieza_rotada, x, y, jugador):
                                        return True
                                elif self.es_adyacente_diagonal(pieza_rotada, x, y, colocadas, jugador):
                                    return True
        return False
     #con esto se determina si el juego acabo validando si hay uno de los jugadores puede jugar
     #si ningun jugador puede jugar el juego acaba
    def juego_terminado(self,colocadas,jugador1,jugador2,limite_fichas):
        piezas_j1_colocadas = self.filtrar_colocadas_por_jugador(colocadas,jugador1)
        piezas_j2_colocadas = self.filtrar_colocadas_por_jugador(colocadas,jugador2)
        sin_mov_j1 = len(piezas_j1_colocadas) >= limite_fichas
        sin_mov_j2 = len(piezas_j2_colocadas) >= limite_fichas      
        return sin_mov_j1 and sin_mov_j2
      

    def mostrar_resultado(self, puntajes, nombre_jugador2= "Jugador 2"):
        puntos_j1 = puntajes.get("Jugador 1", 0)
        puntos_j2 = puntajes.get("Jugador 2", puntajes.get("Jugador 2 (IA)", 0))

        print("\n=== Resultado Final ===")
        print(f"Puntaje Jugador 1: {puntos_j1}")
        print(f"Puntaje {nombre_jugador2}: {puntos_j2}")

        if puntos_j1 > puntos_j2:
           print("¡Jugador 1 es el ganador!")
        elif puntos_j2 > puntos_j1:
           print(f"¡{nombre_jugador2} es el ganador!")
        else:
          print("¡Empate!")





