import subprocess
import os
import readchar
from colorama import init, Fore, Style

# Inicializa colorama
init(autoreset=True)

# Solo se mantienen las opciones "JUGAR" y "SALIR"
opciones = [
    ("🎮", "JUGAR", Fore.GREEN),
    ("📴", "SALIR", Fore.RED)
]

ANCHO_TOTAL = 20

def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")

def mostrar_menu(indice_seleccionado):
    limpiar_pantalla()
    titulo = "MENÚ PRINCIPAL"
    padding = (ANCHO_TOTAL - 2 - len(titulo)) // 2

    # --- Inicio de la modificación ---

    # Dibuja el borde solo para el título
    print(Fore.CYAN + "╔" + "═" * (ANCHO_TOTAL - 2) + "╗")
    print("║" + " " * padding + Fore.WHITE + Style.BRIGHT + titulo + Style.RESET_ALL + Fore.CYAN + " " * (ANCHO_TOTAL - 2 - padding - len(titulo)) + "║")
    print("╚" + "═" * (ANCHO_TOTAL - 2) + "╝" + Style.RESET_ALL)
    
    print() # Añade un espacio para separar el título de las opciones

    # Muestra las opciones sin el borde lateral
    for i, (icono, texto, color) in enumerate(opciones):
        flecha = "▶" if i == indice_seleccionado else " "
        linea = f"{flecha} {icono} {texto}"
        # Se ajusta el padding para alinear las opciones debajo del título
        print(color + " " * 2 + linea + Style.RESET_ALL)

    # --- Fin de la modificación ---

def ejecutar_opcion(indice):
    limpiar_pantalla()
    texto = opciones[indice][1]
    if texto == "JUGAR":
        # Asegúrate de que la ruta a tablero.py sea correcta si está en otro directorio
        ruta_tablero = os.path.join(os.path.dirname(__file__), "tablero.py")
        try:
            subprocess.run(["python", ruta_tablero], check=True)
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {ruta_tablero}")
        except subprocess.CalledProcessError:
            print("Hubo un error al ejecutar el juego.")
        input("\nPresiona Enter para continuar...")
    elif texto == "SALIR":
        print("¡Hasta luego!")
        exit()

def main():
    indice = 0
    while True:
        mostrar_menu(indice)
        tecla = readchar.readkey()
        if tecla == readchar.key.UP:
            indice = (indice - 1) % len(opciones)
        elif tecla == readchar.key.DOWN:
            indice = (indice + 1) % len(opciones)
        elif tecla == readchar.key.ENTER:
            ejecutar_opcion(indice)
        elif tecla == 'q': # Opcional: una forma de salir si el menú se bloquea
            break

if __name__ == "__main__":
    main()