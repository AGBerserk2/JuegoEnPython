from menu import Menu  
from movimiento import Movimiento 
import keyboard 
import os  
  
def guardar_historial(puntajes):  
    with open("historial.txt", "a") as f:  
        f.write(f"Puntajes: {puntajes}\n") 

   
  
if __name__ == "__main__":  
    
     while True:  
        opcion_seleccionada = Menu.mostrar_menu()  
        termino = False

        if opcion_seleccionada == 1:  # Jugar vs Humano  
            juego = Movimiento(modo_ia=False)  
            termino = juego.movimiento_tablero()
            if termino:
             # Guardar puntajes al finalizar  
             puntajes = {  
                "Jugador 1": juego.score.obtener_puntos("Jugador 1"),  
                "Jugador 2": juego.score.obtener_puntos("Jugador 2")  
            }  
             
            juego.logica.mostrar_resultado(puntajes)
            guardar_historial(puntajes) 
            
            input("\nPresiona cualquier tecla para continuar")
            while keyboard.is_pressed("enter"):
             pass

        elif opcion_seleccionada == 2:  # Jugar vs IA  
            juego = Movimiento(modo_ia=True)  
            termino = juego.movimiento_tablero()
            if termino:
                 # Guardar puntajes al finalizar  
             puntajes = {  
                "Jugador 1": juego.score.obtener_puntos("Jugador 1"),  
                "Jugador 2 (IA)": juego.score.obtener_puntos("Jugador 2")  
             } 
            juego.logica.mostrar_resultado(puntajes) 
            guardar_historial(puntajes) 
            
            input("\nPresiona cualquier tecla para continuar") 
            while keyboard.is_pressed("enter"):
               pass


 
        elif opcion_seleccionada == 3:  # Historial  
            os.system('cls' if os.name == 'nt' else 'clear')  
            try:  
                 with open("historial.txt", "r") as f:  
                    print("=== Historial de Partidas ===")  
                    print(f.read())  
            except FileNotFoundError:  
                print("No hay historial de partidas.")  
            input("Presiona Enter para continuar...")  

        elif opcion_seleccionada == 4:  # Salir  
            os.system('cls' if os.name == 'nt' else 'clear')  
            print("¿Seguro que quieres salir? (s/n)")  
            if input().lower() == 's':  
                break