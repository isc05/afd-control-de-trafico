class TrafficAutomaton:
    """
    Autómata Finito Determinista para validar la secuencia estricta de configuración
    de un semáforo inteligente.
    Exige de manera obligatoria al menos un carácter de tiempo 't' entre cada fase de color.
    Alfabeto: {v, a, r, t}
    """
    def __init__(self):
        self.states = {'q0', 'qV', 'qVt', 'qA', 'qAt', 'qR', 'qRt', 'q_err'}
        self.initial_state = 'q0'
        self.final_states = {'qRt'}
        self.current_state = self.initial_state
        
        self.transitions = {
            ('q0', 'v'): 'qV',
            ('qV', 't'): 'qVt',
            ('qVt', 't'): 'qVt',
            ('qVt', 'a'): 'qA',
            ('qA', 't'): 'qAt',
            ('qAt', 't'): 'qAt',
            ('qAt', 'r'): 'qR',
            ('qR', 't'): 'qRt',
            ('qRt', 't'): 'qRt',
            ('qRt', 'v'): 'qV'
        }

    def process_char(self, char: str) -> str:
        """
        Procesa un carácter de entrada y evalúa la transición de estado.
        Cualquier transición no definida conduce al estado de error q_err.
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
        Determina si el estado actual es un estado de aceptación (qRt).
        """
        return self.current_state in self.final_states

    def extract_timings(self, input_string: str) -> dict:
        """
        Calcula la cantidad acumulada de unidades de tiempo 't'
        asignadas a cada fase de color dentro de una cadena aceptada.
        """
        timings = {'v': 0, 'a': 0, 'r': 0}
        current_color = None
        
        for char in input_string.lower():
            if char in ['v', 'a', 'r']:
                current_color = char
            elif char == 't' and current_color:
                timings[current_color] += 1
                
        return timings