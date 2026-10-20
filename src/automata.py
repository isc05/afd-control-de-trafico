class TrafficAutomaton:
    """
    Autómata Finito Determinista para validar cadenas de configuración
    de un semáforo inteligente.
    Alfabeto: {v, a, r, t}
    """
    def __init__(self):
        self.states = {'q0', 'qV', 'qA', 'qR', 'q_err'}
        self.initial_state = 'q0'
        self.final_states = {'qR'}
        self.current_state = self.initial_state
        
        self.transitions = {
            ('q0', 'v'): 'qV',
            ('qV', 't'): 'qV',
            ('qV', 'a'): 'qA',
            ('qA', 't'): 'qA',
            ('qA', 'r'): 'qR',
            ('qR', 't'): 'qR',
            ('qR', 'v'): 'qV' 
        }

    def process_char(self, char: str) -> str:
        """
        Procesa un carácter de entrada y evalúa la transición de estado.
        """
        char = char.lower()
        if (self.current_state, char) in self.transitions:
            self.current_state = self.transitions[(self.current_state, char)]
        else:
            self.current_state = 'q_err'
            
        return self.current_state

    def reset(self):
        """
        Restablece el autómata a su estado inicial.
        """
        self.current_state = self.initial_state

    def is_accepted(self) -> bool:
        """
        Determina si el estado actual es un estado de aceptación.
        """
        return self.current_state in self.final_states

    def extract_timings(self, input_string: str) -> dict:
        """
        Extrae la cantidad de 't' (tiempos) asignados a cada color a partir
        de una cadena válida.
        """
        timings = {'v': 0, 'a': 0, 'r': 0}
        current_color = None
        
        for char in input_string.lower():
            if char in ['v', 'a', 'r']:
                current_color = char
            elif char == 't' and current_color:
                timings[current_color] += 1
                
        return timings