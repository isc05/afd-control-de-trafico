"""
Módulo gui.py
Controla la interfaz gráfica de usuario y la renderización del grafo con matplotlib.
"""

import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.automata import AutomataTrafico

class InterfazAutomata:
    """Clase principal de la interfaz gráfica."""

    def __init__(self, root):
        """
        Inicializa la ventana principal y los componentes gráficos.
        
        Args:
            root (tk.Tk): La ventana raíz de tkinter.
        """
        self.root = root
        self.root.title("Simulador AFD - Control de Tráfico")
        self.root.geometry("800x700")
        
        self.automata = AutomataTrafico()
        
        self.configurar_interfaz()
        self.configurar_grafo()
        self.dibujar_grafo('q0', 'neutral')

    def configurar_interfaz(self):
        """Configura los elementos de control y visualización de la ventana."""
        frame_controles = tk.Frame(self.root)
        frame_controles.pack(pady=10)

        tk.Label(frame_controles, text="Cadena de entrada (use 't' para temporizador):").grid(row=0, column=0, padx=5)
        self.entry_entrada = tk.Entry(frame_controles, width=30)
        self.entry_entrada.grid(row=0, column=1, padx=5)

        self.btn_evaluar = tk.Button(frame_controles, text="Evaluar Entrada", command=self.iniciar_evaluacion)
        self.btn_evaluar.grid(row=0, column=2, padx=5)

        self.lbl_estado = tk.Label(self.root, text="Esperando entrada...", font=("Arial", 12, "bold"))
        self.lbl_estado.pack(pady=5)

        self.txt_transiciones = tk.Text(self.root, height=5, width=80, state=tk.DISABLED)
        self.txt_transiciones.pack(pady=5)

        self.frame_grafo = tk.Frame(self.root)
        self.frame_grafo.pack(fill=tk.BOTH, expand=True)

    def configurar_grafo(self):
        """Configura la estructura estática del grafo usando NetworkX."""
        self.grafo = nx.DiGraph()
        self.grafo.add_nodes_from(self.automata.estados)
        
        for origen, trans in self.automata.transiciones.items():
            for simbolo, destino in trans.items():
                self.grafo.add_edge(origen, destino, label=simbolo)
        
        # Conexiones hacia el estado de error para visualización
        for estado in ['q0', 'q1', 'q2', 'q3']:
            self.grafo.add_edge(estado, 'q_err', label='otro')

        self.posiciones = {
            'q0': (0, 1),
            'q1': (1, 1),
            'q2': (1, 0),
            'q3': (0, 0),
            'q_err': (0.5, 0.5)
        }

        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_grafo)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def dibujar_grafo(self, estado_activo, estado_validacion):
        """
        Renderiza el grafo actualizando los colores según el estado de la validación.
        
        Args:
            estado_activo (str): El identificador del nodo que debe resaltarse.
            estado_validacion (str): 'neutral', 'valido' o 'invalido' para determinar el esquema de colores.
        """
        self.ax.clear()
        
        colores_nodos = []
        for nodo in self.grafo.nodes():
            if nodo == estado_activo:
                colores_nodos.append('yellow')
            elif estado_validacion == 'valido':
                colores_nodos.append('lightgreen')
            elif estado_validacion == 'invalido':
                colores_nodos.append('salmon')
            else:
                colores_nodos.append('lightblue')

        nx.draw(self.grafo, self.posiciones, ax=self.ax, with_labels=True, 
                node_color=colores_nodos, node_size=2000, font_size=10, 
                font_weight='bold', arrows=True, arrowsize=20)
        
        etiquetas_aristas = nx.get_edge_attributes(self.grafo, 'label')
        nx.draw_networkx_edge_labels(self.grafo, self.posiciones, ax=self.ax, edge_labels=etiquetas_aristas)
        
        self.canvas.draw()

    def registrar_transicion(self, mensaje):
        """Añade un mensaje al cuadro de texto de historial."""
        self.txt_transiciones.config(state=tk.NORMAL)
        self.txt_transiciones.insert(tk.END, mensaje + "\n")
        self.txt_transiciones.see(tk.END)
        self.txt_transiciones.config(state=tk.DISABLED)

    def iniciar_evaluacion(self):
        """Prepara el autómata y la interfaz para iniciar el procesamiento de la entrada."""
        entrada = self.entry_entrada.get()
        if not entrada:
            messagebox.showwarning("Advertencia", "Debe ingresar una cadena.")
            return

        self.btn_evaluar.config(state=tk.DISABLED)
        self.txt_transiciones.config(state=tk.NORMAL)
        self.txt_transiciones.delete(1.0, tk.END)
        self.txt_transiciones.config(state=tk.DISABLED)
        
        self.automata.reiniciar()
        self.registrar_transicion(f"Inicio en el estado: {self.automata.estado_actual}")
        self.dibujar_grafo(self.automata.estado_actual, 'neutral')
        
        self.lbl_estado.config(text="Procesando...", fg="black")
        
        # Iniciar la animación paso a paso
        self.root.after(1000, self.procesar_paso, entrada, 0)

    def procesar_paso(self, cadena, indice):
        """
        Función recursiva gestionada por temporizador para procesar la cadena carácter por carácter.
        
        Args:
            cadena (str): Cadena completa proporcionada por el usuario.
            indice (int): Posición del carácter actual siendo procesado.
        """
        if indice < len(cadena):
            caracter = cadena[indice]
            estado_anterior = self.automata.estado_actual
            nuevo_estado = self.automata.procesar_caracter(caracter)
            
            self.registrar_transicion(f"Entrada '{caracter}': Transición {estado_anterior} -> {nuevo_estado}")
            self.dibujar_grafo(nuevo_estado, 'neutral')
            
            self.root.after(1000, self.procesar_paso, cadena, indice + 1)
        else:
            self.finalizar_evaluacion()

    def finalizar_evaluacion(self):
        """Determina la validez del recorrido final y actualiza los indicadores visuales."""
        es_valido = self.automata.es_valido()
        
        if es_valido:
            self.lbl_estado.config(text="Entrada VÁLIDA. Autómata aceptado.", fg="green")
            self.dibujar_grafo(self.automata.estado_actual, 'valido')
        else:
            self.lbl_estado.config(text="Entrada NO VÁLIDA. Estado de error alcanzado.", fg="red")
            self.dibujar_grafo(self.automata.estado_actual, 'invalido')
            
        self.btn_evaluar.config(state=tk.NORMAL)