class IntelligentTrafficAutomaton:
    """
    Automata Finito Determinista dinámico que representa la logica de control de un
    semaforo inteligente. Evalua eventos de tiempo y longitud de colas vehiculares
    para decidir las transiciones de estado y optimizar el flujo.
    """

    def __init__(self):
        self.states = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5'}
        self.initial_state = 'q0'
        self.final_states = set()
        self.current_state = self.initial_state

    def evaluate_transition(self, queue_ns: int, queue_ew: int) -> str:
        """
        Determina el siguiente estado del automata basandose en el estado actual y
        la evaluacion del trafico en la interseccion (filas N-S vs E-O).
        
        Args:
            queue_ns: Cantidad de vehiculos esperando en la via Norte-Sur.
            queue_ew: Cantidad de vehiculos esperando en la via Este-Oeste.
            
        Returns:
            El identificador del nuevo estado activo.
        """
        if self.current_state == 'q0':
            self.current_state = 'q1'
            
        elif self.current_state == 'q1':
            if queue_ns >= queue_ew:
                self.current_state = 'q0'
            else:
                self.current_state = 'q2'
                
        elif self.current_state == 'q2':
            self.current_state = 'q3'
            
        elif self.current_state == 'q3':
            self.current_state = 'q4'
            
        elif self.current_state == 'q4':
            if queue_ew >= queue_ns:
                self.current_state = 'q3'
            else:
                self.current_state = 'q5'
                
        elif self.current_state == 'q5':
            self.current_state = 'q0'

        return self.current_state

    def reset(self):
        """
        Devuelve el automata a su estado inicial.
        """
        self.current_state = self.initial_state