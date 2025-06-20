
import os
import keyboard
from colorama import init, Fore, Style

init(autoreset=True)  # Inicializa colorama

class Menu:
    selected_index = 0
    options = [
        "    • Jugar",
        "    • Historial",
        "    • Salir 🔚"
    ]
    
    color_fondo = Fore.WHITE
    color_seleccionado = Fore.CYAN + Style.BRIGHT
    color_texto = Fore.RED

    @classmethod
    def mostrar_menu(cls):
        key_pressed = None
        while key_pressed != 'enter':
            os.system('cls' if os.name == 'nt' else 'clear')
            cls.mostrar_opciones()
            
            # Esperar por una tecla
            while True:
                if keyboard.is_pressed('up'):
                    cls.selected_index = (cls.selected_index - 1) % len(cls.options)
                    while keyboard.is_pressed('up'): pass  # Esperar a que se suelte la tecla
                    break
                elif keyboard.is_pressed('down'):
                    cls.selected_index = (cls.selected_index + 1) % len(cls.options)
                    while keyboard.is_pressed('down'): pass  # Esperar a que se suelte la tecla
                    break
                elif keyboard.is_pressed('enter'):
                    key_pressed = 'enter'
                    break
        
        return cls.selected_index + 1
    
    @classmethod
    def mostrar_opciones(cls):
        # Mostrar el título ASCII
        print(Fore.RED + """

                                            ▀█████████▄   ▄█        ▄██████▄     ▄█   ▄█▄ ███    █▄     ▄████████ 
                                              ███    ███ ███       ███    ███   ███ ▄███▀ ███    ███   ███    ███ 
                                              ███    ███ ███       ███    ███   ███▐██▀   ███    ███   ███    █▀  
                                             ▄███▄▄▄██▀  ███       ███    ███  ▄█████▀    ███    ███   ███        
                                            ▀▀███▀▀▀██▄  ███       ███    ███ ▀▀█████▄    ███    ███ ▀███████████ 
                                              ███    ██▄ ███       ███    ███   ███▐██▄   ███    ███          ███ 
                                              ███    ███ ███▌    ▄ ███    ███   ███ ▀███▄ ███    ███    ▄█    ███ 
                                            ▄█████████▀  █████▄▄██  ▀██████▀    ███   ▀█▀ ████████▀   ▄████████▀  
                                                         ▀                      ▀                                                                                                                          
""")
        
        print(cls.color_fondo + """
                                     ╔═════════════════════════════════════════════════════════════════════════════════╗
                                     ║                                ¿Modo de juego?                                  ║
                                     ║                      🔷 ---     Lets  START!!!    --- 🔷                        ║
                                     ║                                                                                 ║
                                     ╚═════════════════════════════════════════════════════════════════════════════════╝

                                                  ╔═══════════════════════════════════════════════════╗""")

        # Mostrar opciones
        for i, option in enumerate(cls.options):
            if i == cls.selected_index:
                print("                                                            🕹️ " + cls.color_seleccionado + option)
            else:
                print("                                                              " + cls.color_texto + option)
        
        print(cls.color_fondo + """                                                  ╚═══════════════════════════════════════════════════╝

                                    ═══════════════════════════════════════════════════════════════════════════════════
                                              🟥 Usa las Flechas para Navegar y Enter para Seleccionar 🟥
                                 ═══════════════════════════════════════════════════════════════════════════════════════════
                                    """)
        print(Style.RESET_ALL)

# Ejemplo de uso
if __name__ == "__main__":
    opcion_seleccionada = Menu.mostrar_menu()
    print(f"\nOpción seleccionada: {opcion_seleccionada}")
