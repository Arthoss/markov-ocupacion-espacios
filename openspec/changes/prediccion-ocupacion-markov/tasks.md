## 1. Base del proyecto

- [x] 1.1 Crear el proyecto Django `config` en la raíz y la app `ocupacion`
- [x] 1.2 Configurar `settings.py`: registrar `ocupacion`, `LANGUAGE_CODE = "es-co"`, `TIME_ZONE = "America/Bogota"`
- [x] 1.3 Crear `pytest.ini` con `DJANGO_SETTINGS_MODULE = config.settings` y la carpeta `tests/`
- [x] 1.4 Crear una prueba de humo que verifique que pytest y Django funcionan

## 2. Modelo de Markov (`markov/core.py`) con TDD

- [x] 2.1 Escribir en `tests/test_core.py` las pruebas de validación de la matriz y del vector (escenarios de la spec)
- [ ] 2.2 Implementar `MatrizInvalidaError`, `validar_matriz` y `validar_vector` hasta que pasen las pruebas
- [x] 2.3 Escribir las pruebas de `predecir`, `predecir_pasos` y `evolucion` (1, 3 y 10 pasos con los valores de la spec)
- [ ] 2.4 Implementar `predecir`, `predecir_pasos` y `evolucion` hasta que pasen las pruebas
- [x] 2.5 Escribir las pruebas de `distribucion_estacionaria` (valor esperado y π · P = π)
- [ ] 2.6 Implementar `distribucion_estacionaria` hasta que pasen las pruebas

## 3. Gestión de escenarios

- [ ] 3.1 Crear el modelo `Escenario` con `clean()` que use `markov.core` y su migración
- [ ] 3.2 Crear la migración de datos con el escenario "Salón 101"
- [ ] 3.3 Crear `EscenarioForm` (estados separados por comas, matriz una fila por línea) con sus validaciones
- [ ] 3.4 Escribir `tests/test_forms.py` con los escenarios de la spec (nombres repetidos, matriz inválida)
- [ ] 3.5 Implementar las vistas, rutas y plantillas de listar, crear, editar y eliminar
- [ ] 3.6 Escribir en `tests/test_views.py` las pruebas del CRUD y del escenario precargado

## 4. Visualización de resultados

- [ ] 4.1 Implementar la vista de detalle con el selector de estado inicial (`?estado_inicial=`)
- [ ] 4.2 Mostrar la matriz de transición y la tabla de resultados para 1, 3, 5 y 10 pasos en porcentaje
- [ ] 4.3 Pasar los datos a la plantilla con `json_script` y dibujar la gráfica de líneas (pasos 0 a 10) con Chart.js
- [ ] 4.4 Dibujar la gráfica de barras agrupadas para los pasos 1, 3, 5 y 10
- [ ] 4.5 Mostrar la distribución estacionaria y resaltar el estado más probable a largo plazo
- [ ] 4.6 Escribir las pruebas de la página de resultados (tabla, datos de las gráficas, estado más probable)

## 5. Cierre

- [ ] 5.1 Aplicar estilos básicos y una plantilla base con navegación
- [ ] 5.2 Ejecutar toda la suite de pruebas y corregir los fallos
- [ ] 5.3 Actualizar `requirements.txt` y escribir el `README.md` (instalación, uso, pruebas, proceso SDD)