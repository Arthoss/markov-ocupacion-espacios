"""Operaciones matemáticas puras para cadenas de Markov."""

import numpy as np


class MatrizInvalidaError(ValueError):
    """Error lanzado cuando una matriz de transición no es válida."""


def validar_matriz(P):
    """Valida que P sea cuadrada, de al menos 3x3 y estocástica por filas.

    Cada elemento debe pertenecer a [0, 1] y cada fila debe cumplir
    |suma(fila) - 1| <= 1e-6.
    """
    try:
        matriz = np.asarray(P, dtype=float)
    except (TypeError, ValueError) as error:
        raise MatrizInvalidaError(
            "La matriz debe contener filas numéricas del mismo tamaño."
        ) from error

    if matriz.ndim != 2:
        raise MatrizInvalidaError("La matriz de transición debe ser cuadrada.")

    filas, columnas = matriz.shape
    if filas != columnas:
        raise MatrizInvalidaError("La matriz de transición debe ser cuadrada.")
    if filas < 3:
        raise MatrizInvalidaError("Se requieren mínimo 3 estados.")
    if not np.all(np.isfinite(matriz)) or np.any((matriz < 0) | (matriz > 1)):
        raise MatrizInvalidaError("Los valores deben estar entre 0 y 1.")

    for indice, fila in enumerate(matriz, start=1):
        if not np.isclose(np.sum(fila), 1.0, atol=1e-6, rtol=0.0):
            raise MatrizInvalidaError(f"La fila {indice} no suma 1.")


def validar_vector(v, n):
    """Valida que v tenga n probabilidades en [0, 1] cuya suma sea 1."""
    try:
        vector = np.asarray(v, dtype=float)
    except (TypeError, ValueError) as error:
        raise ValueError("El vector inicial debe contener valores numéricos.") from error

    if vector.ndim != 1 or len(vector) != n:
        raise ValueError(f"El vector inicial debe tener {n} valores.")
    if not np.all(np.isfinite(vector)) or np.any((vector < 0) | (vector > 1)):
        raise ValueError("Los valores del vector inicial deben estar entre 0 y 1.")
    if not np.isclose(np.sum(vector), 1.0, atol=1e-6, rtol=0.0):
        raise ValueError("El vector inicial debe sumar 1.")


def predecir(P, v0, n):
    """Calcula π(n) = π(0) · Pⁿ para n pasos desde el vector inicial v0."""
    validar_matriz(P)
    matriz = np.asarray(P, dtype=float)
    validar_vector(v0, matriz.shape[0])

    if isinstance(n, bool) or not isinstance(n, (int, np.integer)) or n < 0:
        raise ValueError("El número de pasos debe ser un entero no negativo.")

    distribucion = np.asarray(v0, dtype=float) @ np.linalg.matrix_power(matriz, n)
    return distribucion.tolist()


def predecir_pasos(P, v0, pasos=(1, 3, 5, 10)):
    """Calcula π(0) · Pⁿ y devuelve la distribución para cada n solicitado."""
    return {paso: predecir(P, v0, paso) for paso in pasos}


def evolucion(P, v0, hasta=10):
    """Calcula π(k) = π(0) · Pᵏ para cada paso k desde 0 hasta ``hasta``."""
    validar_matriz(P)
    matriz = np.asarray(P, dtype=float)
    validar_vector(v0, matriz.shape[0])

    if (
        isinstance(hasta, bool)
        or not isinstance(hasta, (int, np.integer))
        or hasta < 0
    ):
        raise ValueError("El número de pasos debe ser un entero no negativo.")

    distribuciones = [np.asarray(v0, dtype=float)]
    for _ in range(hasta):
        distribuciones.append(distribuciones[-1] @ matriz)

    return [distribucion.tolist() for distribucion in distribuciones]


def distribucion_estacionaria(P):
    """Calcula π como vector propio de Pᵀ para λ = 1, normalizado para sumar 1."""
    validar_matriz(P)
    matriz = np.asarray(P, dtype=float)

    valores, vectores = np.linalg.eig(matriz.T)
    indice = int(np.argmin(np.abs(valores - 1)))
    estacionaria = np.real(vectores[:, indice])
    suma = np.sum(estacionaria)

    if np.isclose(suma, 0.0):
        raise ValueError("No se pudo normalizar la distribución estacionaria.")

    estacionaria = estacionaria / suma
    return estacionaria.tolist()
