## ADDED Requirements

### Requirement: Validación de la matriz de transición
El sistema DEBE (MUST) validar que la matriz de transición sea cuadrada, tenga
al menos 3 estados, contenga solo valores entre 0 y 1, y que cada fila sume 1
con una tolerancia de 0.000001.

#### Scenario: Matriz válida
- **GIVEN** la matriz [[0.50, 0.35, 0.15], [0.25, 0.45, 0.30], [0.10, 0.35, 0.55]]
- **WHEN** se valida la matriz
- **THEN** la validación es exitosa

#### Scenario: Fila que no suma 1
- **GIVEN** una matriz cuya primera fila es [0.50, 0.30, 0.10]
- **WHEN** se valida la matriz
- **THEN** se rechaza con un mensaje que indica que la fila 1 no suma 1

#### Scenario: Valor negativo
- **GIVEN** una matriz con un valor de -0.10
- **WHEN** se valida la matriz
- **THEN** se rechaza indicando que los valores deben estar entre 0 y 1

#### Scenario: Menos de 3 estados
- **GIVEN** una matriz de 2x2
- **WHEN** se valida la matriz
- **THEN** se rechaza indicando que se requieren mínimo 3 estados

#### Scenario: Matriz no cuadrada
- **GIVEN** una matriz de 3 filas y 4 columnas
- **WHEN** se valida la matriz
- **THEN** se rechaza indicando que la matriz debe ser cuadrada

### Requirement: Predicción a n pasos
El sistema DEBE (MUST) calcular la distribución de probabilidad después de n
pasos con la fórmula π(n) = π(0) · Pⁿ, donde π(0) es el vector de estado inicial.

#### Scenario: Predicción a 1 paso desde Libre
- **GIVEN** la matriz de ejemplo y el estado inicial Libre, vector [1, 0, 0]
- **WHEN** se calcula la predicción a 1 paso
- **THEN** el resultado es [0.5000, 0.3500, 0.1500]

#### Scenario: Predicción a 3 pasos desde Libre
- **GIVEN** la matriz de ejemplo y el estado inicial Libre
- **WHEN** se calcula la predicción a 3 pasos
- **THEN** el resultado redondeado a 4 decimales es [0.2988, 0.3885, 0.3128]

#### Scenario: El resultado es una distribución válida
- **GIVEN** cualquier matriz válida y cualquier vector inicial válido
- **WHEN** se calcula la predicción a n pasos
- **THEN** las probabilidades del resultado suman 1

#### Scenario: Vector inicial inválido
- **GIVEN** un vector inicial [0.5, 0.2, 0.1] que no suma 1
- **WHEN** se intenta calcular la predicción
- **THEN** se rechaza indicando que el vector inicial debe sumar 1

### Requirement: Predicción para los pasos de referencia
El sistema DEBE (MUST) calcular en una sola operación las predicciones para
1, 3, 5 y 10 pasos.

#### Scenario: Cálculo de los pasos de referencia
- **GIVEN** la matriz de ejemplo y el estado inicial Libre
- **WHEN** se calculan las predicciones de referencia
- **THEN** se obtienen resultados para 1, 3, 5 y 10 pasos
- **AND** el resultado a 10 pasos redondeado a 4 decimales es [0.2639, 0.3889, 0.3472]

### Requirement: Distribución estacionaria
El sistema DEBE (MUST) calcular la distribución estacionaria π que cumple
π · P = π y cuya suma es 1.

#### Scenario: Estacionaria de la matriz de ejemplo
- **GIVEN** la matriz de ejemplo
- **WHEN** se calcula la distribución estacionaria
- **THEN** el resultado redondeado a 4 decimales es [0.2639, 0.3889, 0.3472]

#### Scenario: La estacionaria no cambia al multiplicar por P
- **GIVEN** la distribución estacionaria π de una matriz válida P
- **WHEN** se calcula π · P
- **THEN** el resultado es igual a π con una tolerancia de 0.0001