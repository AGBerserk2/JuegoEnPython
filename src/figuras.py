# creacion de todas las figuras
# ya

class figuras():
    def dibujar_pieza(pieza):
        for fila in pieza:
            print(''.join('⬜' if celda == 1 else '  ' for celda in fila))
        print()  # Espacio entre piezas

    def piezas():
    # 1. Monomino
        monomino = [[1]]
        # 2. Domino
        domino = [[1, 1]]
        # 3. Tromino en línea
        tromino_line = [[1, 1, 1]]
        # 4. Tromino en L
        tromino_L = [
            [1, 0],
            [1, 1]
        ]
        # 5. Tetromino en L
        tetromino_L = [
            [1, 0, 0],
            [1, 1, 1]
        ]
        # 6. Tetromino en T
        tetromino_T = [
            [1, 1, 1],
            [0, 1, 0]
        ]
        # 7. Tetromino cuadrado
        tetromino_square = [
            [1, 1],
            [1, 1]
        ]
        # 8. Tetromino en Z
        tetromino_Z = [
            [1, 1, 0],
            [0, 1, 1]
        ]
        # 9. Pentomino en línea
        pentomino_line = [[1, 1, 1, 1, 1]]
        # 10. Pentomino cruz
        pentomino_plus = [
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0]
        ]