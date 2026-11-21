## ADDED Requirements

### Requirement: Selección del estado inicial
El sistema DEBE (MUST) permitir elegir el estado inicial de un escenario para
calcular sus predicciones.

#### Scenario: Cálculo desde un estado elegido
- **GIVEN** el escenario "Salón 101"
- **WHEN** el usuario elige el estado inicial "Lleno" y presiona Calcular
- **THEN** se muestran las predicciones calculadas desde el vector [0, 0, 1]

### Requirement: Tabla de resultados
El sistema DEBE (MUST) mostrar una tabla con la probabilidad de cada estado
para 1, 3, 5 y 10 pasos, expresada en porcentaje con 2 decimales.

#### Scenario: Tabla de predicciones
- **GIVEN** el escenario "Salón 101" con el estado inicial Libre
- **WHEN** se calculan las predicciones
- **THEN** la tabla muestra 4 filas (1, 3, 5 y 10 pasos) y una columna por estado
- **AND** la fila de 1 paso muestra 50.00 %, 35.00 % y 15.00 %

### Requirement: Gráfica de evolución
El sistema DEBE (MUST) mostrar una gráfica de líneas con la probabilidad de
cada estado desde el paso 0 hasta el paso 10.

#### Scenario: Gráfica de líneas
- **GIVEN** unas predicciones calculadas
- **WHEN** se muestra la página de resultados
- **THEN** aparece una gráfica de líneas con una línea por estado y 11 puntos (pasos 0 a 10)

### Requirement: Gráfica comparativa por pasos
El sistema DEBE (MUST) mostrar una gráfica de barras que compare la
distribución de probabilidad en los pasos 1, 3, 5 y 10.

#### Scenario: Gráfica de barras
- **GIVEN** unas predicciones calculadas
- **WHEN** se muestra la página de resultados
- **THEN** aparece una gráfica de barras agrupadas por paso (1, 3, 5 y 10) con una barra por estado

### Requirement: Distribución estacionaria e interpretación
El sistema DEBE (MUST) mostrar la distribución estacionaria y resaltar el
estado más probable a largo plazo.

#### Scenario: Interpretación a largo plazo
- **GIVEN** el escenario "Salón 101"
- **WHEN** se muestran los resultados
- **THEN** se muestra la distribución estacionaria [26.39 %, 38.89 %, 34.72 %]
- **AND** se resalta "Medio" como el estado más probable a largo plazo