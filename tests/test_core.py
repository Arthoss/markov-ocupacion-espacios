import pytest

from markov.core import (
    MatrizInvalidaError,
    distribucion_estacionaria,
    evolucion,
    predecir,
    predecir_pasos,
    validar_matriz,
    validar_vector,
)


@pytest.fixture
def matriz_ejemplo():
    return [
        [0.50, 0.35, 0.15],
        [0.25, 0.45, 0.30],
        [0.10, 0.35, 0.55],
    ]


def test_matriz_valida(matriz_ejemplo):
    """Matriz válida."""
    validar_matriz(matriz_ejemplo)


def test_fila_que_no_suma_1(matriz_ejemplo):
    """Fila que no suma 1."""
    matriz_ejemplo[0] = [0.50, 0.30, 0.10]

    with pytest.raises(MatrizInvalidaError, match=r"fila 1.*suma 1"):
        validar_matriz(matriz_ejemplo)


def test_valor_negativo(matriz_ejemplo):
    """Valor negativo."""
    matriz_ejemplo[0][0] = -0.10

    with pytest.raises(MatrizInvalidaError, match=r"entre 0 y 1"):
        validar_matriz(matriz_ejemplo)


def test_menos_de_3_estados():
    """Menos de 3 estados."""
    with pytest.raises(MatrizInvalidaError, match=r"mínimo 3 estados"):
        validar_matriz([[0.5, 0.5], [0.5, 0.5]])


def test_matriz_no_cuadrada():
    """Matriz no cuadrada."""
    with pytest.raises(MatrizInvalidaError, match=r"cuadrada"):
        validar_matriz(
            [
                [0.25, 0.25, 0.25, 0.25],
                [0.25, 0.25, 0.25, 0.25],
                [0.25, 0.25, 0.25, 0.25],
            ]
        )


def test_prediccion_a_1_paso_desde_libre(matriz_ejemplo):
    """Predicción a 1 paso desde Libre."""
    resultado = predecir(matriz_ejemplo, [1, 0, 0], 1)

    assert resultado == pytest.approx([0.5000, 0.3500, 0.1500], abs=1e-4)


def test_prediccion_a_3_pasos_desde_libre(matriz_ejemplo):
    """Predicción a 3 pasos desde Libre."""
    resultado = predecir(matriz_ejemplo, [1, 0, 0], 3)

    assert resultado == pytest.approx([0.2988, 0.3885, 0.3128], abs=1e-4)


def test_el_resultado_es_una_distribucion_valida(matriz_ejemplo):
    """El resultado es una distribución válida."""
    resultado = predecir(matriz_ejemplo, [1, 0, 0], 5)

    assert sum(resultado) == pytest.approx(1.0, abs=1e-4)


def test_vector_inicial_invalido(matriz_ejemplo):
    """Vector inicial inválido."""
    with pytest.raises(ValueError, match=r"vector inicial debe sumar 1"):
        predecir(matriz_ejemplo, [0.5, 0.2, 0.1], 1)


def test_calculo_de_los_pasos_de_referencia(matriz_ejemplo):
    """Cálculo de los pasos de referencia."""
    resultados = predecir_pasos(matriz_ejemplo, [1, 0, 0])

    assert set(resultados) == {1, 3, 5, 10}
    assert resultados[1] == pytest.approx([0.5000, 0.3500, 0.1500], abs=1e-4)
    assert resultados[3] == pytest.approx([0.2988, 0.3885, 0.3128], abs=1e-4)
    assert resultados[5] == pytest.approx([0.2694, 0.3889, 0.3417], abs=1e-4)
    assert resultados[10] == pytest.approx([0.2639, 0.3889, 0.3472], abs=1e-4)


def test_evolucion_de_la_distribucion(matriz_ejemplo):
    """Evolución de la distribución."""
    resultados = evolucion(matriz_ejemplo, [1, 0, 0], hasta=10)

    assert len(resultados) == 11
    assert resultados[0] == pytest.approx([1.0, 0.0, 0.0], abs=1e-4)
    assert resultados[1] == pytest.approx([0.5000, 0.3500, 0.1500], abs=1e-4)
    assert resultados[3] == pytest.approx([0.2988, 0.3885, 0.3128], abs=1e-4)
    assert resultados[10] == pytest.approx([0.2639, 0.3889, 0.3472], abs=1e-4)


def test_estacionaria_de_la_matriz_de_ejemplo(matriz_ejemplo):
    """Estacionaria de la matriz de ejemplo."""
    resultado = distribucion_estacionaria(matriz_ejemplo)

    assert resultado == pytest.approx([0.2639, 0.3889, 0.3472], abs=1e-4)


def test_la_estacionaria_no_cambia_al_multiplicar_por_p(matriz_ejemplo):
    """La estacionaria no cambia al multiplicar por P."""
    estacionaria = distribucion_estacionaria(matriz_ejemplo)
    resultado = [
        sum(estacionaria[i] * matriz_ejemplo[i][j] for i in range(3))
        for j in range(3)
    ]

    assert resultado == pytest.approx(estacionaria, abs=1e-4)
