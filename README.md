# Sistema Inteligente de Tráfico con AFD

Aplicación de escritorio educativa que combina un autómata finito determinista (AFD) con una simulación visual simplificada de una intersección. Primero se valida una secuencia de configuración de las luces; si la cadena es aceptada, se puede simular el tránsito de vehículos con esos tiempos y una densidad seleccionable.

> Esta aplicación es una demostración académica. Su modelo simplificado no es un controlador de tráfico real ni está diseñado para tomar decisiones de seguridad vial.

## Qué hace

### Validación de la configuración

El AFD representa las fases del semáforo para el sentido norte-sur:

| Estado | Fase | Transiciones |
| --- | --- | --- |
| `q0` | Inicio | `v` → `qV` |
| `qV` | Verde | `t` → `qV`; `a` → `qA` |
| `qA` | Amarillo | `t` → `qA`; `r` → `qR` |
| `qR` | Rojo | `t` → `qR`; `v` → `qV` para iniciar otro ciclo |
| `q_err` | Error | Estado al que llega cualquier símbolo sin transición válida |

- `v`, `a` y `r` representan verde, amarillo y rojo.
- `t` representa un intervalo de tiempo en la fase actual; repetirlo alarga esa fase.
- La cadena debe comenzar con `v`, seguir las fases en orden y terminar en `qR`, el único estado de aceptación. Por ejemplo, `vttatrtt` es válida: asigna dos intervalos al verde, uno al amarillo y dos al rojo.
- Las mayúsculas se aceptan porque los símbolos se convierten a minúsculas. Cualquier otro símbolo lleva la cadena al estado de error.
- La interfaz muestra el recorrido por el AFD paso a paso y señala si la configuración fue aceptada.

### Simulación de la intersección

Después de validar una cadena, el botón **Simular Tráfico** permite ver una intersección con circulación norte-sur y este-oeste. Los intervalos `t` contados para cada color determinan la duración de las fases. Se puede seleccionar una densidad de sensores **Baja**, **Media** o **Alta**; la llegada de vehículos y sus colores se generan aleatoriamente.

La simulación anima los vehículos, aplica las luces y una distancia de seguridad simplificada, y muestra avisos si detecta una colisión o un atasco severo. Finaliza al completar su número máximo de pasos o antes si detecta una de esas condiciones.

## Requisitos

- Python 3 con soporte para Tkinter.
- No se requieren paquetes externos de Python. `tkinter`, `math` y `random` pertenecen a la biblioteca estándar. En algunas distribuciones de Linux, Tkinter se instala por separado como paquete del sistema (por ejemplo, `python3-tk`).

## Instalación y ejecución

Clona el repositorio y entra en la carpeta del proyecto:

```bash
git clone <URL-del-repositorio>
cd practica3-automatas-finitos-control-trafico
```

Opcionalmente, crea y activa un entorno virtual. En Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

En macOS o Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

`requirements.txt` se conserva para documentar que no hay dependencias instalables con pip. No es necesario instalar paquetes; ejecuta la aplicación con:

```bash
python main.py
```

En Windows también puedes usar `py main.py`. Se abrirá la ventana **Sistema Inteligente de Tráfico - AFD**. Introduce una cadena, selecciona la densidad y pulsa **1. Validar AFD**. Si se acepta, pulsa **2. Simular Tráfico** para iniciar la animación.

## Estructura

```text
.
├── main.py             # Punto de entrada de la aplicación Tkinter
├── requirements.txt    # Indica que no hay dependencias externas de pip
└── src/
    ├── __init__.py
    ├── automata.py     # Estados, transiciones, aceptación y conteo de intervalos
    └── gui.py          # Interfaz, visualización del AFD y simulación de tráfico
```
