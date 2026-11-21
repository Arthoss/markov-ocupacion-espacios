# gestion-escenarios Specification

## Purpose
TBD - created by archiving change prediccion-ocupacion-markov. Update Purpose after archive.

## Requirements

### Requirement: Crear escenario
El sistema DEBE (MUST) permitir crear un escenario con un nombre, una lista de
mínimo 3 estados con nombres únicos y su matriz de transición.

#### Scenario: Creación exitosa
- **GIVEN** el nombre "Laboratorio 2", los estados Libre, Medio y Lleno, y una matriz válida
- **WHEN** el usuario envía el formulario
- **THEN** el escenario se guarda
- **AND** el usuario es redirigido al detalle del escenario

#### Scenario: Estados con nombres repetidos
- **GIVEN** los estados Libre, Libre y Lleno
- **WHEN** el usuario envía el formulario
- **THEN** el escenario no se guarda y se muestra que los nombres de los estados deben ser únicos

#### Scenario: Matriz inválida
- **GIVEN** una matriz con una fila que no suma 1
- **WHEN** el usuario envía el formulario
- **THEN** el escenario no se guarda y se muestra el error de validación de la fila

### Requirement: Escenario de ejemplo precargado
El sistema DEBE (MUST) incluir un escenario de ejemplo llamado "Salón 101" con
los estados Libre, Medio y Lleno y la matriz de ejemplo.

#### Scenario: Primer uso de la aplicación
- **GIVEN** una base de datos recién migrada
- **WHEN** el usuario abre la lista de escenarios
- **THEN** aparece el escenario "Salón 101"

### Requirement: Listar escenarios
El sistema DEBE (MUST) mostrar la lista de escenarios guardados con su nombre y
su número de estados.

#### Scenario: Lista con escenarios
- **GIVEN** existen los escenarios "Salón 101" y "Laboratorio 2"
- **WHEN** el usuario abre la página principal
- **THEN** se muestran ambos escenarios con su número de estados

### Requirement: Editar escenario
El sistema DEBE (MUST) permitir modificar el nombre, los estados y la matriz de
un escenario, aplicando las mismas validaciones que al crearlo.

#### Scenario: Edición válida
- **GIVEN** el escenario "Salón 101"
- **WHEN** el usuario cambia la matriz por otra válida y guarda
- **THEN** el escenario queda actualizado con la nueva matriz

### Requirement: Eliminar escenario
El sistema DEBE (MUST) permitir eliminar un escenario después de una confirmación.

#### Scenario: Eliminación confirmada
- **GIVEN** el escenario "Laboratorio 2"
- **WHEN** el usuario confirma la eliminación
- **THEN** el escenario ya no aparece en la lista
