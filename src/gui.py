import tkinter as tk
from tkinter import ttk, messagebox
import math
import random
from src.automata import IntelligentTrafficAutomaton


class TrafficDFA_GUI:
    """
    Clase que gestiona la representacion visual y concurrente del Automata Finito
    y el flujo fisico de vehiculos en la interseccion.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Semaforo Inteligente - Evaluacion Dinamica mediante AFD")
        self.root.geometry("1300x700")

        self.automaton = IntelligentTrafficAutomaton()
        self.node_radius = 28
        self.is_running = False

        self.setup_ui()
        self.draw_dfa(active_state=self.automaton.initial_state)

    def setup_ui(self):
        """
        Estructura el layout principal dividiendo la pantalla en el panel de control,
        la visualizacion del AFD y el lienzo de simulacion de trafico.
        """
        control_frame = ttk.LabelFrame(self.root, text="Parametros de Simulacion", padding="10")
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(control_frame, text="Temporizador Base (ticks):").grid(row=0, column=0, padx=5)
        self.entry_timer = ttk.Entry(control_frame, width=10)
        self.entry_timer.insert(0, "40")
        self.entry_timer.grid(row=0, column=1, padx=5)

        ttk.Label(control_frame, text="Afluencia Vial (RNG):").grid(row=0, column=2, padx=5)
        self.density_var = tk.StringVar(value="Normal")
        self.cb_density = ttk.Combobox(control_frame, textvariable=self.density_var, 
                                       values=["Poco", "Normal", "Mucho"], state="readonly", width=10)
        self.cb_density.grid(row=0, column=3, padx=5)

        self.lbl_q_ns = ttk.Label(control_frame, text="Fila N-S: 0", font=("Arial", 10, "bold"), foreground="blue")
        self.lbl_q_ns.grid(row=0, column=4, padx=15)

        self.lbl_q_ew = ttk.Label(control_frame, text="Fila E-O: 0", font=("Arial", 10, "bold"), foreground="green")
        self.lbl_q_ew.grid(row=0, column=5, padx=15)

        self.btn_toggle = ttk.Button(control_frame, text="Iniciar Sistema", command=self.toggle_simulation)
        self.btn_toggle.grid(row=0, column=6, padx=15)

        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Panel Izquierdo: AFD Concurrente
        dfa_frame = ttk.LabelFrame(main_container, text="Representacion del AFD")
        dfa_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self.canvas_dfa = tk.Canvas(dfa_frame, bg="white")
        self.canvas_dfa.pack(fill=tk.BOTH, expand=True)

        # Panel Derecho: Simulacion Fisica
        traffic_frame = ttk.LabelFrame(main_container, text="Interseccion de Trafico")
        traffic_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        self.canvas_traffic = tk.Canvas(traffic_frame, bg="#424242", width=600, height=600)
        self.canvas_traffic.pack(fill=tk.BOTH, expand=True)

        self.draw_intersection()

    def draw_dfa(self, active_state: str = None):
        """
        Renderiza el grafo del AFD. Plasma las rutas de transicion descriptivas y 
        colorea el estado actual para reflejar el estado logico del semaforo en tiempo real.
        """
        self.canvas_dfa.delete("all")

        positions = {
            'q0': (150, 100),
            'q1': (500, 100),
            'q2': (500, 250),
            'q3': (500, 400),
            'q4': (150, 400),
            'q5': (150, 250)
        }

        labels = {
            'q0': "q0\nVerde N-S",
            'q1': "q1\nAmarillo N-S",
            'q2': "q2\nRojo Global\n(Despeje N->E)",
            'q3': "q3\nVerde E-O",
            'q4': "q4\nAmarillo E-O",
            'q5': "q5\nRojo Global\n(Despeje E->N)"
        }

        self.draw_edges(positions)

        for state, (x, y) in positions.items():
            fill_color = "#FFF59D" if state == active_state else "#E0E0E0"

            self.canvas_dfa.create_oval(
                x - self.node_radius, y - self.node_radius,
                x + self.node_radius, y + self.node_radius,
                fill=fill_color, outline="black", width=2
            )

            if state == self.automaton.initial_state:
                self.canvas_dfa.create_polygon(
                    x - self.node_radius - 25, y - 10,
                    x - self.node_radius, y,
                    x - self.node_radius - 25, y + 10,
                    fill="blue", outline="black"
                )

            self.canvas_dfa.create_text(x, y, text=labels[state], justify=tk.CENTER, font=("Arial", 8, "bold"))

    def draw_edges(self, pos: dict):
        """
        Dibuja lineas direccionales con textos explicativos que definen las reglas de
        evaluacion inteligente implementadas en el automata.
        """
        def draw_arrow(start, end, label, offset_x=0, offset_y=0):
            x1, y1 = pos[start]
            x2, y2 = pos[end]
            
            x1 += offset_x; y1 += offset_y
            x2 += offset_x; y2 += offset_y
            
            dx, dy = x2 - x1, y2 - y1
            length = math.hypot(dx, dy)
            if length == 0: return

            adj_x1 = x1 + (dx / length) * self.node_radius
            adj_y1 = y1 + (dy / length) * self.node_radius
            adj_x2 = x2 - (dx / length) * self.node_radius
            adj_y2 = y2 - (dy / length) * self.node_radius

            self.canvas_dfa.create_line(adj_x1, adj_y1, adj_x2, adj_y2, arrow=tk.LAST, width=2)
            self.canvas_dfa.create_text((adj_x1 + adj_x2) / 2, ((adj_y1 + adj_y2) / 2) - 15, text=label, fill="blue", font=("Arial", 8, "bold"))

        draw_arrow('q0', 'q1', "Temporizador Expirado", offset_y=-10)
        draw_arrow('q1', 'q0', "Evaluacion Amarilla:\nFila N-S >= Fila E-O\n(Mantiene Prioridad N-S)", offset_y=15)
        draw_arrow('q1', 'q2', "Evaluacion Amarilla:\nFila E-O > Fila N-S\n(Cede Paso a E-O)")
        draw_arrow('q2', 'q3', "Termina Despeje")
        
        draw_arrow('q3', 'q4', "Temporizador Expirado", offset_y=15)
        draw_arrow('q4', 'q3', "Evaluacion Amarilla:\nFila E-O >= Fila N-S\n(Mantiene Prioridad E-O)", offset_y=-15)
        draw_arrow('q4', 'q5', "Evaluacion Amarilla:\nFila N-S > Fila E-O\n(Cede Paso a N-S)")
        draw_arrow('q5', 'q0', "Termina Despeje")

    def toggle_simulation(self):
        """
        Controla el encendido y apagado de la ejecucion concurrente.
        """
        if self.is_running:
            self.is_running = False
            self.btn_toggle.config(text="Iniciar Sistema")
        else:
            try:
                self.timer_limit = int(self.entry_timer.get())
            except ValueError:
                messagebox.showerror("Error", "El temporizador debe ser un numero entero.")
                return

            self.is_running = True
            self.btn_toggle.config(text="Detener Sistema")
            self.entry_timer.config(state=tk.DISABLED)
            
            self.cars = []
            self.state_ticks = 0
            self.automaton.reset()
            self.canvas_traffic.delete("car")
            self.draw_dfa(active_state=self.automaton.current_state)
            self.run_traffic_tick()

    def draw_intersection(self):
        """
        Renderiza las calzadas para la animacion fisica del trafico.
        """
        self.canvas_traffic.create_rectangle(240, 0, 360, 600, fill="#333333", outline="")
        self.canvas_traffic.create_rectangle(0, 240, 600, 360, fill="#333333", outline="")
        self.canvas_traffic.create_line(300, 0, 300, 600, fill="yellow", dash=(10, 10))
        self.canvas_traffic.create_line(0, 300, 600, 300, fill="yellow", dash=(10, 10))

    def update_traffic_lights(self, state: str):
        """
        Sincroniza los focos graficos con el estado del AFD.
        """
        light_map = {
            'q0': ("green", "red"),
            'q1': ("yellow", "red"),
            'q2': ("red", "red"),
            'q3': ("red", "green"),
            'q4': ("red", "yellow"),
            'q5': ("red", "red")
        }
        ns_color, eo_color = light_map.get(state, ("red", "red"))

        self.canvas_traffic.delete("lights")
        self.canvas_traffic.create_oval(210, 210, 230, 230, fill=ns_color, tags="lights")
        self.canvas_traffic.create_oval(370, 370, 390, 390, fill=ns_color, tags="lights")
        self.canvas_traffic.create_oval(210, 370, 230, 390, fill=eo_color, tags="lights")
        self.canvas_traffic.create_oval(370, 210, 390, 230, fill=eo_color, tags="lights")

    def run_traffic_tick(self):
        """
        Bucle maestro de simulacion. Incrementa el temporizador, evalua reglas de encolamiento,
        y delega el cambio de fase al Automata Finito basado en datos reales del sistema.
        """
        if not self.is_running:
            self.entry_timer.config(state=tk.NORMAL)
            return

        # 1. Contabilizacion de las Filas de Trafico
        ns_queue = len([c for c in self.cars if c['dir'] == 'NS' and c['y'] < 220])
        ew_queue = len([c for c in self.cars if c['dir'] == 'EW' and c['x'] < 220])
        
        self.lbl_q_ns.config(text=f"Fila N-S: {ns_queue}")
        self.lbl_q_ew.config(text=f"Fila E-O: {ew_queue}")

        # 2. Control de Estado via Temporizador
        self.state_ticks += 1
        if self.state_ticks >= self.timer_limit:
            next_state = self.automaton.evaluate_transition(ns_queue, ew_queue)
            self.draw_dfa(active_state=next_state)
            self.state_ticks = 0

        current_state = self.automaton.current_state
        self.update_traffic_lights(current_state)

        # 3. Generacion de Vehiculos (RNG Configurable)
        density_map = {"Poco": 0.02, "Normal": 0.05, "Mucho": 0.12}
        spawn_rate = density_map.get(self.density_var.get(), 0.05)
        if random.random() < spawn_rate:
            self.spawn_car()

        # 4. Motor Fisico (Movimiento y Control Anti-Colisiones)
        self.canvas_traffic.delete("car")
        for i, car in enumerate(self.cars):
            can_move = True

            if car['dir'] == 'NS':
                if 210 < car['y'] < 230 and current_state not in ['q0']:
                    can_move = False
            elif car['dir'] == 'EW':
                if 210 < car['x'] < 230 and current_state not in ['q3']:
                    can_move = False

            if can_move:
                for j, other in enumerate(self.cars):
                    if i != j and car['dir'] == other['dir']:
                        if car['dir'] == 'NS' and 0 < other['y'] - car['y'] < 26:
                            can_move = False
                            break
                        elif car['dir'] == 'EW' and 0 < other['x'] - car['x'] < 26:
                            can_move = False
                            break

            if can_move:
                car['x'] += car['dx']
                car['y'] += car['dy']

            self.canvas_traffic.create_rectangle(
                car['x'], car['y'], car['x'] + 22, car['y'] + 22,
                fill=car['color'], outline="black", tags="car"
            )

        self.cars = [c for c in self.cars if 0 <= c['x'] <= 600 and 0 <= c['y'] <= 600]
        self.root.after(40, self.run_traffic_tick)

    def spawn_car(self):
        """
        Inyecta nuevos elementos a la matriz de simulacion considerando disponibilidad de espacio.
        """
        direction = random.choice(['NS', 'EW'])
        color = random.choice(["#3F51B5", "#4CAF50", "#FF9800", "#E91E63", "#00BCD4"])

        if direction == 'NS':
            car = {'x': 265, 'y': 0, 'dx': 0, 'dy': 4, 'dir': 'NS', 'color': color}
        else:
            car = {'x': 0, 'y': 315, 'dx': 4, 'dy': 0, 'dir': 'EW', 'color': color}

        clear_space = True
        for c in self.cars:
            if c['dir'] == direction:
                if direction == 'NS' and c['y'] < 26:
                    clear_space = False
                elif direction == 'EW' and c['x'] < 26:
                    clear_space = False

        if clear_space:
            self.cars.append(car)