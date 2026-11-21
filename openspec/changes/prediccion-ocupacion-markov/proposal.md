## Why

Las instituciones educativas no tienen una forma sencilla de anticipar qué tan
ocupados estarán sus espacios académicos (salones, laboratorios, salas de
cómputo) en las siguientes franjas horarias. Esto genera congestión, espacios
subutilizados y mala planeación.

Una cadena de Markov permite modelar cómo cambia la ocupación de un espacio de
una franja a la siguiente y predecir su estado futuro a partir de una matriz de
transición, con un modelo matemático simple y explicable.

## What Changes

- Se crea una aplicación web en Django para modelar la ocupación de espacios
  académicos con cadenas de Markov.
- El usuario puede definir escenarios con mínimo 3 estados (por defecto: Libre,
  Medio, Lleno) y su matriz de transición.
- El sistema valida que la matriz sea estocástica (filas que suman 1, valores
  entre 0 y 1).
- El sistema calcula la distribución de probabilidad para 1, 3, 5 y 10 pasos a
  partir de un estado inicial, además de la distribución estacionaria.
- Los resultados se muestran en tablas y gráficas (Chart.js).
- Todo el cálculo se cubre con pruebas automatizadas (pytest).

## Capabilities

### New Capabilities
- `modelo-markov`: validación de la matriz de transición, predicción a n pasos
  (π₀ · Pⁿ) y cálculo de la distribución estacionaria.
- `gestion-escenarios`: crear, consultar, editar y eliminar escenarios con sus
  estados y su matriz de transición.
- `visualizacion-resultados`: presentación de las predicciones para 1, 3, 5 y
  10 pasos en tablas y gráficas.

### Modified Capabilities
Ninguna (proyecto nuevo).

## Impact

- Nuevo proyecto Django con una app `ocupacion` y un módulo independiente `markov`.
- Dependencias: Django, NumPy, pytest, pytest-django; Chart.js vía CDN.
- Base de datos SQLite para guardar escenarios.
- Fuera de alcance: autenticación de usuarios, datos reales de sensores y
  despliegue en producción.