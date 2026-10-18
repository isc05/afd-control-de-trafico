"""
Módulo main.py
Punto de entrada de la aplicación.
"""

import tkinter as tk
from src.gui import InterfazAutomata

def main():
    """Función principal que inicializa la interfaz gráfica."""
    root = tk.Tk()
    app = InterfazAutomata(root)
    root.mainloop()

if __name__ == "__main__":
    main()