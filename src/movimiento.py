from figuras import piezas, rotar_pieza  
from AgenteMinimax import AgenteMinimax
from AgenteAleatorio import AgenteAleatorio
from AgenteGreedy import AgenteGreedy

import os  
import time  
import keyboard  
from score import Score  
from logica import Logica  
import random
  
class Movimiento:  
    def __init__(self, modo_ia=False, tipo_ia="minimax", nombre_Ia="IA"):
        self.TABLERO_ALTO = 10
        self.TABLERO_ANCHO = 10  
        self.x, self.y = 0, 0  
        self.pieza = piezas(random.randint(0,9))  
        self.colocadas = []  
        self.jugador_actual = "Jugador 1"  
        self.score = Score()  
        self.score.registrar_jugador("Jugador 1")  
        self.score.registrar_jugador("Jugador 2")  
        self.logica = Logica(self.TABLERO_ANCHO, self.TABLERO_ALTO) 
        self.limite_fichas = 21
        self.modo_ia = modo_ia  # <-- Corrige aquí, antes decía modo_iakj
        self.tipo_ia = tipo_ia.lower()
        self.nombre_jugador2 = nombre_Ia
        self.piezas_disponibles = [piezas(i) for i in range(10)] 

        if self.modo_ia:
          if self.tipo_ia == "minimax":
             self.agente_ia = AgenteMinimax("Jugador 2", self.logica, self.piezas_disponibles, tiempo_limite=2.0)
          elif self.tipo_ia == "aleatorio":
               self.agente_ia = AgenteAleatorio("Jugador 2", self.logica, self.piezas_disponibles)
          elif self.tipo_ia == "greedy":
               self.agente_ia = AgenteGreedy("Jugador 2", self.logica, self.piezas_disponibles)
          else:
             raise ValueError(f"Tipo de IA no reconocido: {self.tipo_ia}")
         



        # Nuevas líneas para IA  
        self.fichas_usadas = {  
        "Jugador 1": [0] * 10,  
        "Jugador 2": [0] * 10  
    }  

    def dibujar_tablero(self):  
        os.system('cls' if os.name == 'nt' else 'clear')  
        tablero = [['⬜' for _ in range(self.TABLERO_ANCHO)] for _ in range(self.TABLERO_ALTO)]  
  
        for p_colocada, px, py, jugador in self.colocadas:  
            for i in range(len(p_colocada)):  
                for j in range(len(p_colocada[0])):  
                    if p_colocada[i][j] == 1:  
                        if 0 <= py + i < self.TABLERO_ALTO and 0 <= px + j < self.TABLERO_ANCHO:  
                            tablero[py + i][px + j] = '🟩' if jugador == "Jugador 1" else '🟥'  
  
        # Solo mostrar pieza actual si NO es turno de IA  
        if not (self.modo_ia and self.jugador_actual == "Jugador 2"):  
            for i in range(len(self.pieza)):  
                for j in range(len(self.pieza[0])):  
                    if self.pieza[i][j] == 1:  
                        if 0 <= self.y + i < self.TABLERO_ALTO and 0 <= self.x + j < self.TABLERO_ANCHO:  
                            tablero[self.y + i][self.x + j] = '🟦'  
  
        for fila in tablero:  
            print(''.join(fila))  
  
        nombre_turno = self.jugador_actual
        if self.jugador_actual == "Jugador 2":
           nombre_turno = self.nombre_jugador2
           print(f"\nTurno de: {nombre_turno}")
        if self.modo_ia and self.jugador_actual == "Jugador 2":
           print(f"🤖 {self.nombre_jugador2} está jugando...") 

        print("Puntaje Jugador 1:", self.score.obtener_puntos("Jugador 1"))  
        print(f"Puntaje {self.nombre_jugador2}:", self.score.obtener_puntos("Jugador 2")) 
  
    def movimiento_tablero(self):  
        while True:  
            self.dibujar_tablero()

            # Verificar si el jugador actual puede jugar
            puede_jugar = self.logica.puede_jugar(self.piezas_disponibles, self.colocadas, self.jugador_actual)
            if not puede_jugar:
                print(f"\n{self.jugador_actual} no puede realizar ningún movimiento.")
                # Determinar ganador por puntaje
                ganador = self.score.determinar_ganador()
                if ganador == "Empate":
                    print("¡No hay más movimientos posibles! El juego termina en empate.")
                else:
                    print(f"¡{ganador} gana automáticamente por no haber más movimientos!")
                input("Presiona enter para salir...")
                exit()  # Termina el programa

            #Esto hace que se salte el turno si el jugador ya ha colcado todas sus fichas
            piezas_jugador = self.logica.filtrar_colocadas_por_jugador(self.colocadas,self.jugador_actual)
            if len(piezas_jugador) >= self.limite_fichas:
                 print(f"{self.limite_fichas} ya se ha colocado el maximo de piezas ({self.limite_fichas}). se salta el turno.")
                 self.jugador_actual = "Jugador 2" if self.jugador_actual == "Jugador 1" else "Jugador 1"

                 time.sleep(1.5)

                 if self.logica.juego_terminado(self.colocadas, "Jugador 1", "Jugador 2", self.limite_fichas):
                    os.system('cls' if os.name == 'nt' else 'clear')
                    self.dibujar_tablero()
                    print("Termino el juego")
                    input("Presiona enter para ver los resultados")
                    time.sleep(1.5)
                    return True
                 continue
              
            # NUEVA LÓGICA: Si es turno de IA, ejecutar movimiento automático  
            if self.modo_ia and self.jugador_actual == "Jugador 2":  
                 self._ejecutar_turno_ia()  
                 continue  
              
            # Código original para jugador humano  
            keyboard.read_event()  
  
            if keyboard.is_pressed('esc'):  
                break  
            elif keyboard.is_pressed('left') and self.x > 0:  
                self.x -= 1  
            elif keyboard.is_pressed('right') and self.x + len(self.pieza[0]) < self.TABLERO_ANCHO:  
                self.x += 1  
            elif keyboard.is_pressed('up') and self.y > 0:  
                self.y -= 1  
            elif keyboard.is_pressed('down') and self.y + len(self.pieza) < self.TABLERO_ALTO:  
                self.y += 1  
            elif keyboard.is_pressed('r'):  
                nueva = rotar_pieza(self.pieza)  
                if self.x + len(nueva[0]) <= self.TABLERO_ANCHO and self.y + len(nueva) <= self.TABLERO_ALTO:  
                    self.pieza = nueva  
                time.sleep(0.2)  
            elif keyboard.is_pressed('space'):  
                piezas_jugador = self.logica.filtrar_colocadas_por_jugador(self.colocadas, self.jugador_actual)  
                turno = len(piezas_jugador)  
                
                # ====== CÓDIGO AGREGADO: Verificar límite de uso de la pieza ======
                indice_pieza_actual = self._identificar_indice_pieza(self.pieza)
                if self.fichas_usadas[self.jugador_actual][indice_pieza_actual] >= 2:
                    print(f"Ya usaste 2 veces la pieza {indice_pieza_actual}. Escoge otra.")
                    time.sleep(1.5)
                    continue

                #De aqui en adelante se establecen los movimientos
                if not self.logica.es_posicion_valida(self.pieza, self.x, self.y, self.colocadas):  
                    print("Posición inválida: la pieza se superpone o está fuera del tablero.")  
                    time.sleep(1)  
                    continue  
  
                if self.logica.es_contacto_lateral(self.pieza, self.x, self.y,self.colocadas,self.jugador_actual):  
                    print("No se permite contacto lateral con tus propias piezas.")  
                    time.sleep(1)  
                    continue  
  
                if turno == 0:  
                    if not self.logica.es_primera_colocacion_valida(self.pieza, self.x, self.y, self.jugador_actual):  
                        print("La primera pieza debe tocar la esquina inicial.")  
                        time.sleep(1)  
                        continue  
                else:  
                    if not self.logica.es_adyacente_diagonal(self.pieza, self.x, self.y,self.colocadas ,self.jugador_actual):  
                        print("Debes colocar la pieza en contacto diagonal con una tuya.")  
                        time.sleep(1)  
                        continue  
  
                # Colocar pieza  
                self.colocadas.append((self.pieza, self.x, self.y, self.jugador_actual))  
                self.score.sumar_puntos_por_pieza(self.jugador_actual, self.pieza) 
                  # CÓDIGO AGREGADO: Aumentar contador de uso de pieza 
                self.fichas_usadas[self.jugador_actual][indice_pieza_actual] += 1
 
                self.pieza = piezas(random.randint(0,9))  
                self.x, self.y = 0, 0  
                self.jugador_actual = "Jugador 2" if self.jugador_actual == "Jugador 1" else "Jugador 1"  
                time.sleep(0.3)  
  
            elif keyboard.is_pressed('c'):  
                os.system('cls' if os.name == 'nt' else 'clear')  
                print("Cambiando ficha...")  
                figura_nueva = self.pedir_figura()  
                self.pieza = piezas(figura_nueva)  
                self.x, self.y = 0, 0 

    # ====== CÓDIGO AGREGADO Y CORREGIDO ======
    def pedir_figura(self):  
        while True:  
            os.system('cls' if os.name == 'nt' else 'clear')  
            print(f"Fichas disponibles para {self.jugador_actual}:\n")  
            disponibles = []  
          
            for i in range(10):  
                if self.fichas_usadas[self.jugador_actual][i] < 2:  
                    disponibles.append(i)  
                    print(f"Opción {i} (Restantes: {2 - self.fichas_usadas[self.jugador_actual][i]}):")  
                    self.dibujar_pieza(piezas(i))  
  
            if not disponibles:  
                print("No hay fichas disponibles. Generando pieza aleatoria.")  
                time.sleep(2)  
                return random.randint(0, 9)  # Fallback a pieza aleatoria  
  
            try:  
                seleccion = int(input("Selecciona el número de la figura: "))  
                if seleccion in disponibles:  
                    return seleccion  
                else:  
                    print("Opción inválida.")  
                    time.sleep(1.5)  
            except ValueError:  
                print("Entrada inválida.")  
                time.sleep(1.5)


         # ====== CÓDIGO AGREGADO: Dibujar pieza en consola ======
    def dibujar_pieza(self, pieza):
        for fila in pieza:
           print(''.join('⬜' if celda == 1 else '  ' for celda in fila))
           print()

    # ====== CÓDIGO AGREGADO: Identificar índice de la pieza actual ======
    def _identificar_indice_pieza(self, pieza_actual):    
        for i in range(10):    
            pieza_original = piezas(i)  # Primero declarar pieza_original  
            pieza_test = pieza_original   # Luego asignarla a pieza_test  
              
            for _ in range(4):    
                if pieza_actual == pieza_test:    
                    return i    
                pieza_test = rotar_pieza(pieza_test)    
      
        print(f"Advertencia: No se pudo identificar la pieza, usando índice 0")    
        return 0
    
    # NUEVO MÉTODO: Lógica para el turno de la IA  
    def _ejecutar_turno_ia(self): 
        print(f"{self.nombre_jugador2} está pensando...")  
        piezas_ia = self.logica.filtrar_colocadas_por_jugador(self.colocadas, self.jugador_actual)
        if len(piezas_ia) >= self.limite_fichas:
            print(f"{self.nombre_jugador2} ya colocó el máximo de piezas. Se pasa el turno.")
            self.jugador_actual = "Jugador 1"
            return
        
        time.sleep(1.5)  # Pausa dramática  
           
        mejor_movimiento = self.agente_ia.encontrar_mejor_jugada(
            self.colocadas,
            self.fichas_usadas["Jugador 2"]
        )

        if mejor_movimiento:
            pieza, x, y = mejor_movimiento
            self.colocadas.append((pieza, x, y, self.jugador_actual))
            self.score.sumar_puntos_por_pieza(self.jugador_actual, pieza)
            index_pieza = self._identificar_indice_pieza(pieza)
            self.fichas_usadas[self.jugador_actual][index_pieza] += 1
            print(f"🤖 {self.nombre_jugador2} colocó pieza en posición ({x}, {y})")
        else:
            print(f"🤖 {self.nombre_jugador2} no puede hacer más movimientos")
            self.jugador_actual = "Jugador 1"

        self.jugador_actual = "Jugador 1"
        time.sleep(2)  # Mostrar resultado  
  
    # NUEVO MÉTODO: Algoritmo de decisión de la IA  
    def _encontrar_mejor_movimiento_ia(self):  
        mejores_movimientos = []  
          
        # Usar las mismas piezas disponibles que el sistema original  
        for i in range(10): 
            if self.fichas_usadas[self.jugador_actual][i] >= 2:
               continue 
            pieza = piezas(i)  
            for rot in range(4):  # Probar 4 rotaciones  
                pieza_rotada = pieza  
                for _ in range(rot):  
                    pieza_rotada = rotar_pieza(pieza_rotada)  
                  
                # Probar todas las posiciones del tablero  
                for y in range(self.TABLERO_ALTO):  
                    for x in range(self.TABLERO_ANCHO):  
                        if self._es_movimiento_valido_ia(pieza_rotada, x, y):  
                            puntos = sum(celda == 1 for fila in pieza_rotada for celda in fila)  
                            mejores_movimientos.append((pieza_rotada, x, y, puntos,i))  
          
        if mejores_movimientos:  
            # Ordenar por puntos y tomar el mejor  
            mejores_movimientos.sort(key=lambda x: x[3], reverse=True)  
            mejor = mejores_movimientos[0]
            self.fichas_usadas[self.jugador_actual][mejor[4]] += 1
            return mejor[:3]  # pieza, x, y  
      
  
    # NUEVO MÉTODO: Validación de movimientos para IA  
    def _es_movimiento_valido_ia(self, pieza, x, y):  
        # Usar la misma lógica de validación que el juego original  
        if not self.logica.es_posicion_valida(pieza, x, y, self.colocadas):  
            return False  
        if self.logica.es_contacto_lateral(pieza, x, y, self.colocadas, self.jugador_actual):  
            return False  
          
        piezas_jugador = self.logica.filtrar_colocadas_por_jugador(self.colocadas, self.jugador_actual)  
        turno = len(piezas_jugador)  
          
        if turno == 0:  
            return self.logica.es_primera_colocacion_valida(pieza, x, y, self.jugador_actual)  
        else:  
            return self.logica.es_adyacente_diagonal(pieza, x, y, self.colocadas, self.jugador_actual)



