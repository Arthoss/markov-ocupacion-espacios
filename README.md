# Markov · Ocupación de espacios

Aplicación web en Django para crear escenarios de ocupación de espacios
académicos y estimar la probabilidad de cada estado en pasos futuros.

## El problema

La ocupación variable de salones, laboratorios y otros espacios académicos
dificulta su planeación: algunos lugares se congestionan mientras otros quedan
subutilizados. Esta aplicación permite definir estados de ocupación y modelar
los cambios entre ellos para explorar posibles ocupaciones futuras.

## Cadenas de Markov

Una cadena de Markov representa un sistema que cambia entre estados. La
probabilidad del siguiente estado depende del estado actual y de una matriz de
transición `P`; cada fila de la matriz corresponde al estado actual y cada
columna al estado siguiente. Las probabilidades de cada fila deben sumar 1.

La distribución después de `n` pasos se calcula como:

**π(n) = π(0) · Pⁿ**

`π(0)` es la distribución inicial y `Pⁿ` es la matriz de transición elevada a
la potencia `n`. La distribución estacionaria representa las probabilidades a
largo plazo cuando cumple `π · P = π`.

### Ejemplo: Salón 101

La aplicación precarga este escenario:

| Estado actual \ Siguiente | Libre | Medio | Lleno |
|---|---:|---:|---:|
| Libre | 0.50 | 0.35 | 0.15 |
| Medio | 0.25 | 0.45 | 0.30 |
| Lleno | 0.10 | 0.35 | 0.55 |

Desde el estado inicial **Libre**, las predicciones son:

| Pasos | Libre | Medio | Lleno |
|---:|---:|---:|---:|
| 1 | 50.00 % | 35.00 % | 15.00 % |
| 3 | 29.88 % | 38.85 % | 31.28 % |
| 5 | 26.94 % | 38.89 % | 34.17 % |
| 10 | 26.39 % | 38.89 % | 34.72 % |

La distribución estacionaria es **26.39 % Libre, 38.89 % Medio y 34.72 %
Lleno**. A largo plazo, el estado más probable es **Medio**.

## Tecnologías

- Python y Django
- NumPy para las operaciones matriciales
- SQLite para almacenar escenarios
- pytest, pytest-django y pytest-cov para pruebas y cobertura
- Chart.js para las gráficas (se carga desde CDN y requiere internet)

## Estructura del proyecto

```text
config/                 Configuración y rutas principales de Django
markov/core.py          Validación y cálculos puros de cadenas de Markov
ocupacion/              Modelos, formularios, vistas, rutas y plantillas
ocupacion/migrations/   Esquema y escenario inicial de ejemplo
static/css/              Estilos de la aplicación
templates/               Plantilla base
tests/                   Pruebas de Markov, formularios y vistas
docs/capturas/           Imágenes de la aplicación
```

## Instalación en Windows

Abre PowerShell en la carpeta del proyecto. Se recomienda Python 3.14, usado
para ejecutar las pruebas de este proyecto.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Abre <http://127.0.0.1:8000/> para usar la aplicación. La primera migración
crea el escenario de ejemplo **Salón 101**.

## Uso

1. En Inicio, abre el escenario **Salón 101** o elige **Nuevo escenario**.
2. Escribe un nombre y al menos tres estados separados por comas, por ejemplo
   `Libre, Medio, Lleno`.
3. Ingresa la matriz de transición con una fila por línea. Separa valores por
   espacios o comas y usa punto para los decimales. Cada fila debe sumar 1.
4. Guarda el escenario. Desde el detalle puedes editarlo o eliminarlo.
5. Elige un estado inicial y presiona **Calcular** para consultar las
   predicciones a 1, 3, 5 y 10 pasos, la evolución y la distribución
   estacionaria.

## Pruebas y cobertura

Activa el entorno virtual y ejecuta la suite:

```powershell
python -m pytest
```

Para medir la cobertura del módulo matemático y la aplicación:

```powershell
python -m pytest --cov=markov --cov=ocupacion --cov-report=term-missing
```

## Proceso SDD con OpenSpec

El desarrollo sigue un flujo de especificación por diseño (SDD):

1. **proposal**: describe el problema, los objetivos y el alcance.
2. **specs**: define capacidades y escenarios de comportamiento verificables.
3. **design**: registra decisiones de arquitectura e implementación.
4. **tasks**: divide el cambio en tareas pequeñas y trazables.
5. **Implementación con agente de IA (GitHub Copilot)**: aplica las tareas
   aprobadas y mantiene las especificaciones como guía.
6. **archive**: al terminar y revisar el cambio, archiva la propuesta y sus
   especificaciones en OpenSpec.

> El cambio `prediccion-ocupacion-markov` se archivó al cerrar la sección 5
> (commit `f0750db`); sus specs quedaron en `openspec/specs/`.

En la sección 2 se aplicó **TDD**: primero se escribieron las pruebas del núcleo
de Markov y se confirmó el estado rojo porque la implementación aún no existía;
después se implementaron las funciones hasta que las pruebas pasaron (verde).

**Autores:** Daniel Esteban López Castiblanco, …
**Curso:** … · Actividad final de desarrollo con OpenSpec