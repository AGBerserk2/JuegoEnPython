# donde se ejecutara la app

from menu import Menu
from movimiento import Movimiento
import os

def guardar_historial(puntajes):
    with open("historial.txt", "a") as f:
        f.write(f"Puntajes: {puntajes}\n")

if __name__ == "__main__":
    while True:
        opcion_seleccionada = Menu.mostrar_menu()
        if opcion_seleccionada == 1:  # Jugar
            juego = Movimiento()
            juego.movimiento_tablero()
            # Guardar puntajes al finalizar
            puntajes = {
                "Jugador 1": juego.score.obtener_puntos("Jugador 1"),
                "Jugador 2": juego.score.obtener_puntos("Jugador 2")
            }
            guardar_historial(puntajes)
        elif opcion_seleccionada == 2:  # Historial
            os.system('cls' if os.name == 'nt' else 'clear')
            try:
                with open("historial.txt", "r") as f:
                    print("=== Historial de Partidas ===")
                    print(f.read())
            except FileNotFoundError:
                print("No hay historial de partidas.")
            input("Presiona Enter para continuar...")
        elif opcion_seleccionada == 3:  # Salir
            os.system('cls' if os.name == 'nt' else 'clear')
            print("¿Seguro que quieres salir? (s/n)")
            if input().lower() == 's':
                break


  














