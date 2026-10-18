"""
Módulo automata.py
Implementa la lógica del Autómata Finito Determinista para el control de tráfico.
"""

class AutomataTrafico:
    """
    Clase que representa el AFD del sistema de semáforos.
    
    Estados:
    q0: Verde (N-S), Rojo (E-O)
    q1: Amarillo (N-S), Rojo (E-O)
    q2: Rojo (N-S), Verde (E-O)
    q3: Rojo (N-S), Amarillo (E-O)
    q_err: Estado de error (entrada no válida)
    """

    def __init__(self):
        """Inicializa los componentes formales del AFD."""
        self.estados = ['q0', 'q1', 'q2', 'q3', 'q_err']
        self.alfabeto = ['t']  # 't' representa la expiración del temporizador
        self.estado_inicial = 'q0'
        self.estados_aceptacion = ['q0', 'q1', 'q2', 'q3']
        
        self.transiciones = {
            'q0': {'t': 'q1'},
            'q1': {'t': 'q2'},
            'q2': {'t': 'q3'},
            'q3': {'t': 'q0'}
        }
        
        self.estado_actual = self.estado_inicial
        self.historial_transiciones = []

    def reiniciar(self):
        """Restablece el autómata a su estado inicial para una nueva evaluación."""
        self.estado_actual = self.estado_inicial
        self.historial_transiciones = [(self.estado_inicial, None)]

    def procesar_caracter(self, caracter):
        """
        Procesa un único carácter de entrada y actualiza el estado actual.
        
        Args:
            caracter (str): El símbolo de entrada a procesar.
            
        Returns:
            str: El nuevo estado tras la transición.
        """
        if self.estado_actual == 'q_err':
            self.historial_transiciones.append((self.estado_actual, caracter))
            return self.estado_actual

        estado_siguiente = self.transiciones.get(self.estado_actual, {}).get(caracter)
        
        if estado_siguiente:
            self.estado_actual = estado_siguiente
        else:
            self.estado_actual = 'q_err'
            
        self.historial_transiciones.append((self.estado_actual, caracter))
        return self.estado_actual

    def es_valido(self):
        """
        Verifica si el estado actual al finalizar la cadena es un estado de aceptación.
        
        Returns:
            bool: True si la cadena es válida, False de lo contrario.
        """
        return self.estado_actual in self.estados_aceptacion