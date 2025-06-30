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
            juego = Movimiento(modo_ia=False,tipo_ia="Jugador 2",nombre_Ia= "Jugador 2")  
            termino = juego.movimiento_tablero()
            if termino:
             # Guardar puntajes al finalizar  
              puntajes = {  
                 
                ""
                "Jugador 1": juego.score.obtener_puntos("Jugador 1"),  
                "Jugador 2": juego.score.obtener_puntos("Jugador 2")  
            }  
             
            juego.logica.mostrar_resultado(puntajes)
            guardar_historial(puntajes) 
            
            input("\nPresiona cualquier tecla para continuar")
            while keyboard.is_pressed("enter"):
             pass

        elif opcion_seleccionada == 2:  # Jugar vs IA  
            juego = Movimiento(modo_ia=True, tipo_ia="Simple",nombre_Ia="IA") 
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
           
        elif opcion_seleccionada == 3:
             juego = Movimiento(modo_ia=True, tipo_ia="minimax", nombre_Ia="MiniMax")
             termino = juego.movimiento_tablero()

             if termino:
                 puntajes = {  
                "Jugador 1": juego.score.obtener_puntos("Jugador 1"),  
                "Jugador 2 (IA)": juego.score.obtener_puntos("Jugador 2")  
             } 
                 
             juego.logica.mostrar_resultado(puntajes) 
             guardar_historial(puntajes) 
            
             input("\nPresiona cualquier tecla para continuar") 
             while keyboard.is_pressed("enter"):
               pass
   
       
        elif opcion_seleccionada == 4:  # Jugar vs IA Aleatoria
            juego = Movimiento(modo_ia=True, tipo_ia="aleatorio", nombre_Ia="Aleatorio")
            termino = juego.movimiento_tablero()
            if termino:
             puntajes = {
             "Jugador 1": juego.score.obtener_puntos("Jugador 1"),
             "Jugador 2 (IA)": juego.score.obtener_puntos("Jugador 2")
            }
          
            juego.logica.mostrar_resultado(puntajes, nombre_j2=juego.nombre_jugador2)
            guardar_historial(puntajes)
            input("\nPresiona cualquier tecla para continuar")
            while keyboard.is_pressed("enter"):
              pass 

        elif opcion_seleccionada == 5:  # Jugar vs IA Greedy
             juego = Movimiento(modo_ia=True, tipo_ia="greedy", nombre_Ia="Greedy")
             termino = juego.movimiento_tablero()
             if termino:
              puntajes = {
            "Jugador 1": juego.score.obtener_puntos("Jugador 1"),
            "Jugador 2 (IA)": juego.score.obtener_puntos("Jugador 2")
            }
             juego.logica.mostrar_resultado(puntajes, nombre_j2=juego.nombre_jugador2)
             guardar_historial(puntajes)
             input("\nPresiona cualquier tecla para continuar")
             while keyboard.is_pressed("enter"):
              pass

        elif opcion_seleccionada == 6:  # Historial  
            os.system('cls' if os.name == 'nt' else 'clear')  
            try:  
                 with open("historial.txt", "r") as f:  
                    print("=== Historial de Partidas ===")  
                    print(f.read())  
            except FileNotFoundError:  
                print("No hay historial de partidas.")  
            input("Presiona Enter para continuar...")  

        elif opcion_seleccionada == 7:  # Salir  
            os.system('cls' if os.name == 'nt' else 'clear')  
            print("¿Seguro que quieres salir? (s/n)")  
            if input().lower() == 's':  
                break