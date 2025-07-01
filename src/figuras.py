 
def rotar_pieza(pieza):
    # Transponer y luego invertir filas (rotación 90° horaria)
    return [list(fila) for fila in zip(*pieza[::-1])]
 
def dibujar_pieza(pieza):
    for fila in pieza:
        print(''.join('⬜' if celda == 1 else '  ' for celda in fila))
        print()  # Espacio entre piezas

def piezas (figura):
    match figura:
        case 1:
             return [[1]]
        case 2: 
            return [[1, 1]]
        case 3:
            return  [[1, 1, 1]]
        case 4:
            return   [
                [1, 0],
                [1, 1]
            ]
        case 5:
            return [
                [1, 0, 0],
                [1, 1, 1]
            ]
        case 6:
            return [
                [1,  1, 1],
                [0, 1, 0]
            ]
        case 7:
            return [
                [1, 1],
                [1, 1]
            ]
        case 8:
            return [
                [1, 1, 0],
                [0, 1, 1]
            ]
        case 9:
            return [[1, 1, 1, 1, 1]]
        case 0:
            return [
                [0, 1, 0],
                [1, 1, 1],
                [0, 1, 0]
            ]
        case _:
            return [[1]]