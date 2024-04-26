import tkinter as tk
from tkinter import messagebox
import math

class Gato:
    def __init__(self):
        self.ventana=tk.Tk()
        self.ventana.title("Menu")
        self.ventana.config(width=300, height=200)
        etiqueta1=tk.Label(self.ventana, text = "Selecciona una opcion:", font = "consolas 10", width=30)
        boton1=tk.Button(self.ventana, text = "1. Jugador vs Jugador", font = "consolas 10", width=20, command=lambda: self.jugadorVsJugador())
        boton2=tk.Button(self.ventana, text = "2. Jugador vs IA", font = "consolas 10", width=20, command=lambda: self.jugadorVsIA())
        etiqueta1.place(x=10, y=2)
        boton1.place(x=40, y=40)
        boton2.place(x=40, y=80)

    def jugadorVsIA(self):
        self.ventana_secundaria = tk.Toplevel()
        self.ventana_secundaria.title("Gato")
        self.jugador = "X"
        self.tablero = [[" " for _ in range(3)] for _ in range(3)]
        self.botones = [[None for _ in range(3)] for _ in range(3)]

        for i in range (3):
            for j in range (3):
                self.botones[i][j] = tk.Button(self.ventana_secundaria, text = " ", font = "consolas 30", width=10
                                                    , height=5, command = lambda fila = i, col = j: self.SeleccionarVsIA(fila, col))
                self.botones[i][j].grid(row=i, column=j)

    def jugadorVsJugador(self):
        self.ventana_secundaria = tk.Toplevel()
        self.ventana_secundaria.title("Gato")
        self.jugador = "X"
        self.tablero = [[" " for _ in range(3)] for _ in range(3)]
        self.botones = [[None for _ in range(3)] for _ in range(3)]

        for i in range (3):
            for j in range (3):
                self.botones[i][j] = tk.Button(self.ventana_secundaria, text = " ", font = "consolas 30", width=10
                                                    , height=5, command = lambda fila = i, col = j: self.SeleccionarVsJugador(fila, col))
                self.botones[i][j].grid(row=i, column=j)
    
    def evaluar_estadoVsJugador(self):
        # Verificar si alguien ganó
        for i in range(3):
            # Filas
            if self.tablero[i][0] == self.tablero[i][1] == self.tablero[i][2] != ' ':
                return 1
            # Columnas
            if self.tablero[0][i] == self.tablero[1][i] == self.tablero[2][i] != ' ':
                return 1
        # Diagonales
        if self.tablero[0][0] == self.tablero[1][1] == self.tablero[2][2] != ' ':
            return 1
        if self.tablero[0][2] == self.tablero[1][1] == self.tablero[2][0] != ' ':
            return 1
        # Si no hay ganador, verificar si hay empate
        if ' ' not in [casilla for fila in self.tablero for casilla in fila]:
            return 0  # Empate
        # Si el juego no ha terminado, devuelve None
        return None

    def evaluate(self):
        for row in self.tablero:
            if row.count(row[0]) == len(row) and row[0] != " ":
                return row[0]

        for col in range(len(self.tablero)):
            if self.tablero[0][col] == self.tablero[1][col] == self.tablero[2][col] and self.tablero[0][col] != " ":
                return self.tablero[0][col]

        if self.tablero[0][0] == self.tablero[1][1] == self.tablero[2][2] and self.tablero[0][0] != " ":
            return self.tablero[0][0]
        if self.tablero[0][2] == self.tablero[1][1] == self.tablero[2][0] and self.tablero[0][2] != " ":
            return self.tablero[0][2]

        if " " not in [cell for row in self.tablero for cell in row]:
            return "tie"

        return None

    def minimax(self, depth, maximizing_player, alpha, beta):
        result = self.evaluate()

        if result is not None:
            if result == "X":
                return -10 + depth, None
            elif result == "O":
                return 10 - depth, None
            else:
                return 0, None

        if maximizing_player:
            max_eval = -math.inf
            best_move = None
            for i in range(3):
                for j in range(3):
                    if self.tablero[i][j] == " ":
                        self.tablero[i][j] = "O"
                        eval, _ = self.minimax(depth + 1, False, alpha, beta)
                        self.tablero[i][j] = " "
                        if eval > max_eval:
                            max_eval = eval
                            best_move = (i, j)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
            return max_eval, best_move
        else:
            min_eval = math.inf
            best_move = None
            for i in range(3):
                for j in range(3):
                    if self.tablero[i][j] == " ":
                        self.tablero[i][j] = "X"
                        eval, _ = self.minimax(depth + 1, True, alpha, beta)
                        self.tablero[i][j] = " "
                        if eval < min_eval:
                            min_eval = eval
                            best_move = (i, j)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
            return min_eval, best_move
    
    def SeleccionarCompu(self):
        _, (fila, col) = self.minimax(0, True, -math.inf, math.inf)
        self.tablero[fila][col] = self.jugador
        self.botones[fila][col]["text"] = self.jugador
        self.botones[fila][col]["state"] = "disabled"
        resultado = self.evaluate()
        if resultado is not None:
            if resultado == "tie":
                messagebox.showinfo("Empate", "Empate", parent=self.ventana_secundaria)
            else:
                messagebox.showinfo("Ganador", f"El jugador {self.jugador} gana", parent=self.ventana_secundaria)
                    

    def SeleccionarVsIA(self, fila, col):
        if self.tablero[fila][col] == " ":
            self.tablero[fila][col] = self.jugador
            self.botones[fila][col]["text"] = self.jugador
            self.botones[fila][col]["state"] = "disabled"
        resultado = self.evaluate()
        if resultado is not None:
            if resultado == "tie":
                messagebox.showinfo("Empate", "Empate", parent=self.ventana_secundaria)
            else:
                messagebox.showinfo("Ganador", f"El jugador {self.jugador} gana", parent=self.ventana_secundaria)
        else:
            self.cambiarJugador()
            self.SeleccionarCompu()
            self.cambiarJugador()

    def SeleccionarVsJugador(self, fila, col):
        if self.tablero[fila][col] == " ":
            self.tablero[fila][col] = self.jugador
            self.botones[fila][col]["text"] = self.jugador
            self.botones[fila][col]["state"] = "disabled"
        resultado = self.evaluar_estadoVsJugador()
        if resultado is not None:
            if resultado:
                messagebox.showinfo("Ganador", f"El jugador {self.jugador} gana", parent=self.ventana_secundaria)
            elif resultado == 0:
                messagebox.showinfo("Empate", "Empate", parent=self.ventana_secundaria)
        else:
            self.cambiarJugador()
    
    def cambiarJugador(self):
        if self.jugador == "X":
            self.jugador = "O"
        else:
            self.jugador = "X"

    def run(self):
        self.ventana.mainloop()
        
if __name__ == "__main__":
    juego = Gato()
    juego.run()