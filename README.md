# Simulador AFD para control de tráfico

Aplicación de escritorio que simula un autómata finito determinista (AFD) para representar la secuencia de un semáforo en una intersección. La interfaz permite introducir una cadena, procesarla paso a paso y visualizar tanto las transiciones como el estado del autómata.

## Funcionamiento

El autómata modela dos sentidos de circulación, norte-sur (N-S) y este-oeste (E-O). Su alfabeto contiene un único símbolo:

- `t`: expiración del temporizador del semáforo.

Cada `t` avanza el ciclo de luces:

| Estado | Semáforo N-S | Semáforo E-O | Siguiente estado con `t` |
| --- | --- | --- | --- |
| `q0` | Verde | Rojo | `q1` |
| `q1` | Amarillo | Rojo | `q2` |
| `q2` | Rojo | Verde | `q3` |
| `q3` | Rojo | Amarillo | `q0` |
| `q_err` | Estado de error | Estado de error | `q_err` |

El estado inicial es `q0`. Los estados `q0`, `q1`, `q2` y `q3` son de aceptación; una entrada que contenga un símbolo distinto de `t` lleva al estado de error y es rechazada. En la interfaz se debe ingresar una cadena no vacía, por ejemplo `tttt`.

La aplicación presenta un grafo de estados, resalta el estado actual, registra cada transición y procesa la entrada con una pausa de un segundo entre pasos. Al terminar, indica si la entrada fue aceptada.

## Estructura del proyecto

```text
.
├── main.py             # Punto de entrada; crea la ventana y ejecuta el bucle de Tkinter
├── requirements.txt    # Dependencias de Python
└── src/
    ├── __init__.py
    ├── automata.py     # Estados, alfabeto y lógica de transición del AFD
    └── gui.py          # Interfaz Tkinter y visualización del grafo
```

## Requisitos

- Python 3 instalado y disponible como `python` (en Windows también puede usarse `py`).
- Tkinter, necesario para la interfaz gráfica. En Windows suele venir incluido con la instalación estándar de Python; en Linux puede requerir el paquete del sistema `python3-tk`.
- Las dependencias listadas en `requirements.txt`: Matplotlib y NetworkX, junto con sus dependencias.

## Instalación y ejecución

Clona el repositorio y entra en la carpeta del proyecto:

```bash
git clone <URL-del-repositorio>
cd practica3-automatas-finitos-control-trafico
```

Crea y activa un entorno virtual. En Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

En macOS o Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instala las dependencias y ejecuta la aplicación:

```bash
python -m pip install -r requirements.txt
python main.py
```

En Windows, si no activaste el entorno virtual, puedes ejecutar sus herramientas con rutas directas:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

Se abrirá la ventana **Simulador AFD - Control de Tráfico**. Escribe una cadena formada únicamente por `t` y selecciona **Evaluar Entrada** para observar el recorrido.
