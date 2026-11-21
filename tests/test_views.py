import pytest
from django.urls import reverse

from ocupacion.models import Escenario

pytestmark = pytest.mark.django_db


ESTADOS = "Libre, Medio, Lleno"
MATRIZ = "0.50 0.35 0.15\n0.25 0.45 0.30\n0.10 0.35 0.55"


def datos_formulario(**sobrescrituras):
    datos = {
        "nombre": "Laboratorio 2",
        "estados": ESTADOS,
        "matriz": MATRIZ,
    }
    datos.update(sobrescrituras)
    return datos


def test_lista_muestra_escenario_precargado_y_numero_de_estados(client):
    """Primer uso de la aplicación y lista con escenarios."""
    respuesta = client.get(reverse("ocupacion:lista"))

    assert respuesta.status_code == 200
    assert "Salón 101" in respuesta.content.decode()
    assert "3 estados" in respuesta.content.decode()
    assert respuesta.context["escenarios"].filter(nombre="Salón 101").exists()


def test_creacion_exitosa_redirige_al_detalle(client):
    """Creación exitosa."""
    respuesta = client.post(reverse("ocupacion:crear"), datos_formulario())

    escenario = Escenario.objects.get(nombre="Laboratorio 2")
    assert respuesta.status_code == 302
    assert respuesta.url == reverse("ocupacion:detalle", args=[escenario.pk])
    assert escenario.estados == ["Libre", "Medio", "Lleno"]
    assert escenario.matriz[0] == [0.50, 0.35, 0.15]


@pytest.mark.parametrize(
    ("datos", "mensaje"),
    [
        (
            datos_formulario(estados="Libre, Libre, Lleno"),
            "nombres de los estados deben ser únicos",
        ),
        (
            datos_formulario(
                matriz="0.50 0.30 0.10\n0.25 0.45 0.30\n0.10 0.35 0.55"
            ),
            "fila 1 no suma 1",
        ),
    ],
)
def test_creacion_invalida_muestra_error_y_no_guarda(client, datos, mensaje):
    """Estados con nombres repetidos y matriz inválida."""
    respuesta = client.post(reverse("ocupacion:crear"), datos)

    assert respuesta.status_code == 200
    assert mensaje in respuesta.content.decode()
    assert not Escenario.objects.filter(nombre="Laboratorio 2").exists()


def test_edicion_valida_actualiza_escenario_y_redirige(client):
    """Edición válida."""
    escenario = Escenario.objects.get(nombre="Salón 101")
    nueva_matriz = "0.60 0.25 0.15\n0.20 0.50 0.30\n0.10 0.25 0.65"

    respuesta = client.post(
        reverse("ocupacion:editar", args=[escenario.pk]),
        datos_formulario(nombre="Salón 101 actualizado", matriz=nueva_matriz),
    )

    escenario.refresh_from_db()
    assert respuesta.status_code == 302
    assert respuesta.url == reverse("ocupacion:detalle", args=[escenario.pk])
    assert escenario.nombre == "Salón 101 actualizado"
    assert escenario.matriz[0] == [0.60, 0.25, 0.15]


def test_eliminar_requiere_confirmacion_y_elimina_escenario(client):
    """Eliminación confirmada."""
    escenario = Escenario.objects.get(nombre="Salón 101")
    url = reverse("ocupacion:eliminar", args=[escenario.pk])

    confirmacion = client.get(url)
    assert confirmacion.status_code == 200
    assert "Confirmar eliminación" in confirmacion.content.decode()
    assert Escenario.objects.filter(pk=escenario.pk).exists()

    respuesta = client.post(url)
    assert respuesta.status_code == 302
    assert respuesta.url == reverse("ocupacion:lista")
    assert not Escenario.objects.filter(pk=escenario.pk).exists()


def test_detalle_simple_muestra_nombre_estados_y_matriz(client):
    """El detalle del escenario muestra sus datos básicos."""
    escenario = Escenario.objects.get(nombre="Salón 101")
    respuesta = client.get(reverse("ocupacion:detalle", args=[escenario.pk]))

    assert respuesta.status_code == 200
    assert "Salón 101" in respuesta.content.decode()
    assert "Libre" in respuesta.content.decode()
    assert "0.5" in respuesta.content.decode()
