import pytest

from ocupacion.forms import EscenarioForm
from ocupacion.models import Escenario

pytestmark = pytest.mark.django_db


ESTADOS = "Libre, Medio, Lleno"
MATRIZ_ESPACIOS = "0.50 0.35 0.15\n0.25 0.45 0.30\n0.10 0.35 0.55"


def datos_formulario(**sobrescrituras):
    datos = {
        "nombre": "Laboratorio 2",
        "estados": ESTADOS,
        "matriz": MATRIZ_ESPACIOS,
    }
    datos.update(sobrescrituras)
    return datos


def test_creacion_exitosa():
    """Creación exitosa."""
    formulario = EscenarioForm(data=datos_formulario())

    assert formulario.is_valid(), formulario.errors
    escenario = formulario.save()
    assert escenario.nombre == "Laboratorio 2"
    assert escenario.estados == ["Libre", "Medio", "Lleno"]
    assert escenario.matriz == [
        [0.50, 0.35, 0.15],
        [0.25, 0.45, 0.30],
        [0.10, 0.35, 0.55],
    ]


def test_estados_con_nombres_repetidos():
    """Estados con nombres repetidos."""
    formulario = EscenarioForm(
        data=datos_formulario(estados="Libre, Libre, Lleno")
    )

    assert not formulario.is_valid()
    assert "únicos" in str(formulario.errors["estados"])


def test_matriz_invalida():
    """Matriz inválida."""
    formulario = EscenarioForm(
        data=datos_formulario(
            matriz="0.50 0.30 0.10\n0.25 0.45 0.30\n0.10 0.35 0.55"
        )
    )

    assert not formulario.is_valid()
    assert "fila 1" in str(formulario.errors["matriz"])


def test_matriz_acepta_valores_separados_por_comas():
    """La matriz acepta valores separados por comas."""
    matriz_comas = "0.50, 0.35, 0.15\n0.25, 0.45, 0.30\n0.10, 0.35, 0.55"
    formulario = EscenarioForm(data=datos_formulario(matriz=matriz_comas))

    assert formulario.is_valid(), formulario.errors
    assert formulario.cleaned_data["matriz"][0] == [0.50, 0.35, 0.15]


def test_matriz_rechaza_decimal_con_coma():
    """Los decimales de la matriz deben usar punto."""
    formulario = EscenarioForm(
        data=datos_formulario(
            matriz="0,50 0,35 0,15\n0,25 0,45 0,30\n0,10 0,35 0,55"
        )
    )

    assert not formulario.is_valid()
    assert "matriz" in formulario.errors


def test_edicion_precarga_estados_y_matriz():
    """Al editar se precargan los datos actuales del escenario."""
    escenario = Escenario.objects.get(nombre="Salón 101")

    formulario = EscenarioForm(instance=escenario)

    assert formulario["estados"].value() == "Libre, Medio, Lleno"
    assert formulario["matriz"].value() == MATRIZ_ESPACIOS
