import tkinter as tk
from src.gui import TrafficDFA_GUI

def main():
    """
    Punto de entrada de la aplicación.
    """
    root = tk.Tk()
    app = TrafficDFA_GUI(root)
    root.mainloop()

    
if __name__ == "__main__":
    main()