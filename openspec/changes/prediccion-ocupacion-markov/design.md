## Context

Aplicación web académica para predecir la ocupación de espacios (salones,
laboratorios) con cadenas de Markov. El usuario define escenarios con mínimo 3
estados y su matriz de transición, y consulta predicciones a 1, 3, 5 y 10 pasos
con tablas y gráficas. El proyecto es pequeño, sin autenticación y para uso local.

## Goals / Non-Goals

**Goals:**
- Cálculo de Markov correcto, separado del framework y 100 % probado.
- Interfaz web simple que permita crear escenarios y ver resultados con gráficas.
- Trazabilidad entre escenarios de las specs y pruebas automatizadas.

**Non-Goals:**
- Autenticación de usuarios y roles.
- Datos reales de sensores o estimar la matriz a partir de históricos.
- Despliegue en producción.

## Decisions

### D1. Monolito Django con plantillas
Se usa un solo proyecto Django (`config`) con una app `ocupacion` y plantillas
del lado del servidor.
- **Alternativa descartada:** API REST + frontend separado (React). Duplica el
  trabajo (CORS, dos proyectos, dos suites de pruebas) sin aportar a los
  objetivos del proyecto.

### D2. Lógica de Markov en un módulo puro (`markov/core.py`)
Toda la matemática vive en funciones puras con NumPy, sin importar Django:

| Función | Responsabilidad |
|---|---|
| `validar_matriz(P)` | Verifica que sea cuadrada, mínimo 3x3, valores en [0, 1] y filas que sumen 1 (tolerancia 1e-6). Lanza `MatrizInvalidaError`. |
| `validar_vector(v, n)` | Verifica longitud n, valores en [0, 1] y suma 1. |
| `predecir(P, v0, n)` | Retorna π(n) = π(0) · Pⁿ usando `numpy.linalg.matrix_power`. |
| `predecir_pasos(P, v0, pasos=(1, 3, 5, 10))` | Retorna un diccionario `{paso: distribución}`. |
| `evolucion(P, v0, hasta=10)` | Retorna las distribuciones de los pasos 0 a `hasta` (para la gráfica de líneas). |
| `distribucion_estacionaria(P)` | Retorna π tal que π · P = π y suma 1. |

- **Por qué:** las pruebas del modelo son rápidas, no necesitan base de datos y
  la lógica se puede reutilizar fuera de Django.
- `MatrizInvalidaError` hereda de `ValueError` y su mensaje está en español para
  mostrarlo directamente en el formulario.

### D3. Cálculo de la distribución estacionaria
Se calcula el vector propio de Pᵀ asociado al valor propio 1
(`numpy.linalg.eig`), se toma la parte real y se normaliza para que sume 1.
- **Alternativa:** elevar P a una potencia grande. Se descarta porque es
  aproximada y no converge en cadenas periódicas.

### D4. Modelo de datos con campos JSON
`Escenario` tiene: `nombre` (único), `estados` (JSONField, lista de textos),
`matriz` (JSONField, lista de listas de números), `creado` y `actualizado`.
- **Por qué:** el número de estados es variable; con JSON no se necesitan
  tablas extra de estados y celdas.
- **Trade-off:** la base de datos no valida la matriz, por eso la validación se
  hace en el formulario y en `Escenario.clean()` usando `markov.core`.

### D5. Formulario de escenario
- Estados: un campo de texto separado por comas (`Libre, Medio, Lleno`).
- Matriz: un área de texto con una fila por línea y valores separados por
  espacios o comas.
- El formulario convierte el texto a listas, valida que la matriz tenga tantas
  filas y columnas como estados, que los nombres sean únicos, y llama a
  `validar_matriz`.

### D6. Escenario de ejemplo con migración de datos
Una migración de datos crea "Salón 101" con la matriz
[[0.50, 0.35, 0.15], [0.25, 0.45, 0.30], [0.10, 0.35, 0.55]], para que la app
tenga datos desde el primer uso.

### D7. Rutas
| URL | Vista | Uso |
|---|---|---|
| `/` | Lista de escenarios | Página principal |
| `/escenarios/nuevo/` | Crear | Formulario |
| `/escenarios/<id>/` | Detalle y resultados | Selector de estado inicial por GET (`?estado_inicial=<índice>`), tablas y gráficas |
| `/escenarios/<id>/editar/` | Editar | Formulario |
| `/escenarios/<id>/eliminar/` | Eliminar | Página de confirmación |

### D8. Gráficas con Chart.js
Chart.js se carga por CDN. La vista pasa los datos con el filtro `json_script`
de Django (seguro contra inyección de HTML) y un script en la plantilla dibuja:
- una gráfica de líneas (pasos 0 a 10, una línea por estado);
- una gráfica de barras agrupadas (pasos 1, 3, 5 y 10).

### D9. Estrategia de pruebas
- `tests/test_core.py`: escenarios de la spec `modelo-markov` (valores exactos
  con `pytest.approx`).
- `tests/test_forms.py`: validaciones del formulario.
- `tests/test_views.py`: CRUD, escenario precargado y contenido de la página de
  resultados (con el cliente de pruebas de Django).
- Se escriben las pruebas del modelo **antes** de implementarlo (TDD).

## Risks / Trade-offs

- **Cadenas reducibles** (más de una distribución estacionaria): se toma el
  primer vector propio con valor propio 1. Se documenta como limitación.
- **Errores de redondeo** al ingresar decimales: se usa una tolerancia de 1e-6
  al validar que las filas sumen 1.
- **Chart.js por CDN** requiere internet al ver las gráficas; las tablas
  funcionan sin él.