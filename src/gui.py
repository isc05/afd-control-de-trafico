import tkinter as tk
from tkinter import ttk, messagebox
import math
import random
from src.automata import TrafficAutomaton

class TrafficDFA_GUI:
    """
    Interfaz Gráfica de Usuario que integra la validación del AFD y 
    la simulación del flujo de tráfico en una intersección con colas vehiculares.
    """
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Sistema Inteligente de Tráfico - AFD")
        self.root.geometry("800x650")
        
        self.automaton = TrafficAutomaton()
        self.node_radius = 30
        
        self.setup_ui()
        self.draw_dfa()

    def setup_ui(self):
        control_frame = ttk.LabelFrame(self.root, text="Configuración del Sistema", padding="10")
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(control_frame, text="Cadena (Ej. vttatrtt):").grid(row=0, column=0, padx=5)
        self.entry_input = ttk.Entry(control_frame, width=25)
        self.entry_input.grid(row=0, column=1, padx=5)

        ttk.Label(control_frame, text="Densidad (Sensores):").grid(row=0, column=2, padx=5)
        self.density_var = tk.StringVar(value="Media")
        self.cb_density = ttk.Combobox(control_frame, textvariable=self.density_var, 
                                       values=["Baja", "Media", "Alta"], state="readonly", width=10)
        self.cb_density.grid(row=0, column=3, padx=5)

        self.btn_simulate_dfa = ttk.Button(control_frame, text="1. Validar AFD", command=self.start_dfa_simulation)
        self.btn_simulate_dfa.grid(row=0, column=4, padx=5)

        self.btn_run_traffic = ttk.Button(control_frame, text="2. Simular Tráfico", command=self.start_traffic_simulation, state=tk.DISABLED)
        self.btn_run_traffic.grid(row=0, column=5, padx=5)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.tab_dfa = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_dfa, text="Análisis AFD")

        self.canvas_dfa = tk.Canvas(self.tab_dfa, bg="white", height=300)
        self.canvas_dfa.pack(fill=tk.BOTH, expand=True)

        self.list_log = tk.Listbox(self.tab_dfa, height=6)
        self.list_log.pack(fill=tk.X, side=tk.BOTTOM)

        self.tab_traffic = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_traffic, text="Intersección de Tráfico")

        self.canvas_traffic = tk.Canvas(self.tab_traffic, bg="#555555")
        self.canvas_traffic.pack(fill=tk.BOTH, expand=True)

    def draw_dfa(self, active_state: str = None, final_status: bool = None):
        self.canvas_dfa.delete("all")
        
        positions = {
            'q0': (100, 150),
            'qV': (300, 100),
            'qA': (500, 150),
            'qR': (300, 250),
            'q_err': (100, 250)
        }
        
        labels = {
            'q0': "q0\nInicio",
            'qV': "qV\nVerde",
            'qA': "qA\nAmarillo",
            'qR': "qR\nRojo",
            'q_err': "q_err\nError"
        }

        self.draw_edges(positions)

        base_color = "#E0E0E0" 
        if final_status is True:
            base_color = "#A8E6CF"
        elif final_status is False:
            base_color = "#FF8B94"

        for state, (x, y) in positions.items():
            fill_color = "#FFF59D" if state == active_state else base_color
            
            self.canvas_dfa.create_oval(
                x - self.node_radius, y - self.node_radius, 
                x + self.node_radius, y + self.node_radius, 
                fill=fill_color, outline="black", width=2
            )
            
            if state in self.automaton.final_states:
                offset = 5
                self.canvas_dfa.create_oval(
                    x - self.node_radius + offset, y - self.node_radius + offset, 
                    x + self.node_radius - offset, y + self.node_radius - offset, 
                    outline="black", width=2
                )
            
            if state == self.automaton.initial_state:
                self.canvas_dfa.create_polygon(
                    x - self.node_radius - 30, y - 10,
                    x - self.node_radius, y,
                    x - self.node_radius - 30, y + 10,
                    fill="black"
                )
            
            self.canvas_dfa.create_text(x, y, text=labels[state], justify=tk.CENTER)

    def draw_edges(self, pos: dict):
        transitions = [
            ('q0', 'qV', 'v'), ('qV', 'qA', 'a'), 
            ('qA', 'qR', 'r'), ('qR', 'qV', 'v')
        ]
        
        for start, end, label in transitions:
            x1, y1 = pos[start]
            x2, y2 = pos[end]
            
            dx, dy = x2 - x1, y2 - y1
            length = math.hypot(dx, dy)
            
            if length == 0: continue
                
            x1_adj = x1 + (dx / length) * self.node_radius
            y1_adj = y1 + (dy / length) * self.node_radius
            x2_adj = x2 - (dx / length) * self.node_radius
            y2_adj = y2 - (dy / length) * self.node_radius
            
            self.canvas_dfa.create_line(x1_adj, y1_adj, x2_adj, y2_adj, arrow=tk.LAST, width=2)
            self.canvas_dfa.create_text((x1_adj + x2_adj)/2, (y1_adj + y2_adj)/2 - 10, text=label, fill="blue")

        for state in ['qV', 'qA', 'qR']:
            x, y = pos[state]
            self.canvas_dfa.create_arc(
                x - 20, y - self.node_radius - 30,
                x + 20, y - self.node_radius + 10,
                start=0, extent=270, style=tk.ARC, outline="blue", width=2
            )
            self.canvas_dfa.create_text(x, y - self.node_radius - 20, text='t', fill="blue")

    def start_dfa_simulation(self):
        self.btn_simulate_dfa.config(state=tk.DISABLED)
        self.btn_run_traffic.config(state=tk.DISABLED)
        self.list_log.delete(0, tk.END)
        self.automaton.reset()
        
        self.notebook.select(self.tab_dfa)
        input_string = self.entry_input.get().strip()
        
        self.list_log.insert(tk.END, f"Inicio. Estado: {self.automaton.current_state}")
        self.draw_dfa(active_state=self.automaton.current_state)
        
        if not input_string:
            self.finish_dfa_simulation()
            return

        self.root.after(800, self.simulate_dfa_step, input_string, 0)

    def simulate_dfa_step(self, input_string: str, index: int):
        if index < len(input_string):
            char = input_string[index]
            prev_state = self.automaton.current_state
            new_state = self.automaton.process_char(char)
            
            self.list_log.insert(tk.END, f"Lee '{char}': {prev_state} ---> {new_state}")
            self.list_log.yview(tk.END)
            
            self.draw_dfa(active_state=new_state)
            self.root.after(800, self.simulate_dfa_step, input_string, index + 1)
        else:
            self.finish_dfa_simulation()

    def finish_dfa_simulation(self):
        is_valid = self.automaton.is_accepted()
        
        if is_valid:
            self.list_log.insert(tk.END, "CADENA VÁLIDA. Tiempos configurados correctamente.")
            self.btn_run_traffic.config(state=tk.NORMAL)
        else:
            self.list_log.insert(tk.END, "CADENA INVÁLIDA. Configuración rechazada.")
            
        self.list_log.yview(tk.END)
        self.draw_dfa(active_state=None, final_status=is_valid)
        self.btn_simulate_dfa.config(state=tk.NORMAL)

    def start_traffic_simulation(self):
        self.notebook.select(self.tab_traffic)
        self.canvas_traffic.delete("all")
        self.btn_run_traffic.config(state=tk.DISABLED)
        
        input_string = self.entry_input.get()
        self.timings = self.automaton.extract_timings(input_string)
        
        density_map = {"Baja": 0.02, "Media": 0.05, "Alta": 0.1}
        self.spawn_rate = density_map.get(self.density_var.get(), 0.05)
        
        self.cars = []
        self.simulation_ticks = 0
        self.max_ticks = 300 
        
        self.light_state_NS = 'v'
        self.light_state_EW = 'r'
        self.ticks_in_current_light = 0

        self.draw_intersection()
        self.run_traffic_tick()

    def draw_intersection(self):
        self.canvas_traffic.create_rectangle(340, 0, 460, 600, fill="#333333", outline="")
        self.canvas_traffic.create_rectangle(0, 200, 800, 320, fill="#333333", outline="")
        self.canvas_traffic.create_line(400, 0, 400, 600, fill="yellow", dash=(10, 10))
        self.canvas_traffic.create_line(0, 260, 800, 260, fill="yellow", dash=(10, 10))

    def update_lights(self):
        t_multiplier = 20 
        current_max = self.timings[self.light_state_NS] * t_multiplier
        
        self.ticks_in_current_light += 1
        if self.ticks_in_current_light >= current_max:
            self.ticks_in_current_light = 0
            if self.light_state_NS == 'v':
                self.light_state_NS = 'a'
            elif self.light_state_NS == 'a':
                self.light_state_NS = 'r'
                self.light_state_EW = 'v' 
            elif self.light_state_NS == 'r':
                self.light_state_NS = 'v'
                self.light_state_EW = 'r'

        if self.light_state_NS != 'r':
            self.light_state_EW = 'r'
        elif self.light_state_NS == 'r' and self.light_state_EW != 'a':
            ew_time_passed = self.ticks_in_current_light
            ew_v_limit = self.timings['v'] * t_multiplier
            if ew_time_passed > ew_v_limit:
                self.light_state_EW = 'a'

        colors = {'v': "green", 'a': "yellow", 'r': "red"}
        
        self.canvas_traffic.delete("lights")
        self.canvas_traffic.create_oval(310, 170, 330, 190, fill=colors[self.light_state_NS], tags="lights")
        self.canvas_traffic.create_oval(470, 330, 490, 350, fill=colors[self.light_state_NS], tags="lights")
        
        self.canvas_traffic.create_oval(310, 330, 330, 350, fill=colors[self.light_state_EW], tags="lights")
        self.canvas_traffic.create_oval(470, 170, 490, 190, fill=colors[self.light_state_EW], tags="lights")

    def run_traffic_tick(self):
        if self.simulation_ticks > self.max_ticks:
            messagebox.showinfo("Éxito", "Simulación completada.\nObjetivo cumplido: El tráfico fluyó eficientemente sin accidentes.")
            self.btn_run_traffic.config(state=tk.NORMAL)
            return

        self.simulation_ticks += 1
        self.update_lights()

        if random.random() < self.spawn_rate:
            self.spawn_car()

        self.canvas_traffic.delete("car")
        
        jam_count = 0
        intersection_rect = [340, 200, 460, 320]
        cars_in_intersection = []

        for i, car in enumerate(self.cars):
            can_move = True
            
            # 1. Regla del semáforo
            if car['dir'] == 'NS':
                if 170 < car['y'] < 190 and self.light_state_NS in ['r', 'a']:
                    can_move = False
            elif car['dir'] == 'EW':
                if 310 < car['x'] < 330 and self.light_state_EW in ['r', 'a']:
                    can_move = False

            # 2. Regla de distancia de seguridad (evita solapamiento)
            if can_move:
                for j, other_car in enumerate(self.cars):
                    if i != j and car['dir'] == other_car['dir']:
                        if car['dir'] == 'NS':
                            if 0 < other_car['y'] - car['y'] < 35:
                                can_move = False
                                break
                        elif car['dir'] == 'EW':
                            if 0 < other_car['x'] - car['x'] < 35:
                                can_move = False
                                break

            # 3. Movimiento y atascos
            if can_move:
                car['x'] += car['dx']
                car['y'] += car['dy']
                car['wait_time'] = 0
            else:
                car['wait_time'] += 1
                if car['wait_time'] > 50: 
                    jam_count += 1

            self.canvas_traffic.create_rectangle(
                car['x'], car['y'], car['x']+20, car['y']+20, 
                fill=car['color'], tags="car"
            )

            if (intersection_rect[0] < car['x'] < intersection_rect[2] and 
                intersection_rect[1] < car['y'] < intersection_rect[3]):
                cars_in_intersection.append(car)

        has_ns = any(c['dir'] == 'NS' for c in cars_in_intersection)
        has_ew = any(c['dir'] == 'EW' for c in cars_in_intersection)
        
        if has_ns and has_ew:
            messagebox.showerror("Accidente", "¡Colisión en la intersección!\nLos tiempos configurados no permitieron un cruce seguro.")
            self.btn_run_traffic.config(state=tk.NORMAL)
            return

        if jam_count > 6:
            messagebox.showwarning("Atasco", "¡Atasco de tráfico severo!\nLa cola vehicular excedió la capacidad (tiempo en verde insuficiente).")
            self.btn_run_traffic.config(state=tk.NORMAL)
            return

        self.cars = [c for c in self.cars if 0 <= c['x'] <= 800 and 0 <= c['y'] <= 600]
        self.root.after(50, self.run_traffic_tick)

    def spawn_car(self):
        direction = random.choice(['NS', 'EW'])
        color = random.choice(["#5C6BC0", "#E0E0E0", "#FFA726", "#26C6DA", "#EF5350"])
        
        if direction == 'NS':
            car = {'x': 365, 'y': 0, 'dx': 0, 'dy': 5, 'dir': 'NS', 'color': color, 'wait_time': 0}
        else:
            car = {'x': 0, 'y': 225, 'dx': 5, 'dy': 0, 'dir': 'EW', 'color': color, 'wait_time': 0}
            
        # Solo agregar el coche si no hay otro bloqueando el punto de inicio
        space_clear = True
        for c in self.cars:
            if c['dir'] == direction:
                if direction == 'NS' and c['y'] < 35:
                    space_clear = False
                elif direction == 'EW' and c['x'] < 35:
                    space_clear = False
                    
        if space_clear:
            self.cars.append(car)