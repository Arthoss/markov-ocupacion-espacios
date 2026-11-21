import json
import re

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
    """El detalle del escenario muestra sus datos y resultados."""
    escenario = Escenario.objects.get(nombre="Salón 101")
    respuesta = client.get(reverse("ocupacion:detalle", args=[escenario.pk]))

    assert respuesta.status_code == 200
    assert "Salón 101" in respuesta.content.decode()
    assert "Libre" in respuesta.content.decode()
    assert "0.5" in respuesta.content.decode()


def extraer_json_script(respuesta, identificador):
    html = respuesta.content.decode()
    patron = (
        rf'<script id="{re.escape(identificador)}" type="application/json">'
        r"(.*?)</script>"
    )
    coincidencia = re.search(patron, html)
    assert coincidencia, f"No se encontró el bloque JSON {identificador}"
    return json.loads(coincidencia.group(1))


def test_calculo_desde_estado_inicial_lleno(client):
    """Cálculo desde un estado elegido."""
    escenario = Escenario.objects.get(nombre="Salón 101")
    respuesta = client.get(
        reverse("ocupacion:detalle", args=[escenario.pk]),
        {"estado_inicial": "2"},
    )

    assert respuesta.status_code == 200
    assert respuesta.context["indice_estado_inicial"] == 2
    evolucion = extraer_json_script(respuesta, "datos-evolucion")
    assert evolucion[0] == [0, 0, 1]
    assert evolucion[1] == pytest.approx([0.10, 0.35, 0.55])


def test_tabla_muestra_porcentajes_de_un_paso(client):
    """Tabla de predicciones."""
    escenario = Escenario.objects.get(nombre="Salón 101")
    respuesta = client.get(reverse("ocupacion:detalle", args=[escenario.pk]))

    resultados = respuesta.context["resultados"]
    assert [fila["paso"] for fila in resultados] == [1, 3, 5, 10]
    assert resultados[0]["valores"] == ["50.00 %", "35.00 %", "15.00 %"]


def test_graficas_reciben_evolucion_de_11_pasos_y_pasos_de_referencia(client):
    """Gráfica de líneas y gráfica comparativa por pasos."""
    escenario = Escenario.objects.get(nombre="Salón 101")
    respuesta = client.get(reverse("ocupacion:detalle", args=[escenario.pk]))

    estados = extraer_json_script(respuesta, "datos-estados")
    evolucion = extraer_json_script(respuesta, "datos-evolucion")
    predicciones = extraer_json_script(respuesta, "datos-predicciones")
    assert estados == ["Libre", "Medio", "Lleno"]
    assert len(evolucion) == 11
    assert list(predicciones) == ["1", "3", "5", "10"]
    assert predicciones["1"] == pytest.approx([0.50, 0.35, 0.15])
    assert 'id="grafica-evolucion"' in respuesta.content.decode()
    assert 'id="grafica-predicciones"' in respuesta.content.decode()


def test_distribucion_estacionaria_resalta_medio(client):
    """Interpretación a largo plazo."""
    escenario = Escenario.objects.get(nombre="Salón 101")
    respuesta = client.get(reverse("ocupacion:detalle", args=[escenario.pk]))

    resultados = respuesta.context["resultados_estacionarios"]
    assert [fila["valor"] for fila in resultados] == [
        "26.39 %",
        "38.89 %",
        "34.72 %",
    ]
    assert respuesta.context["estado_mas_probable"] == "Medio"
    assert any(
        fila["estado"] == "Medio" and fila["es_mas_probable"]
        for fila in resultados
    )
    assert "<strong>Medio: 38.89 %</strong>" in respuesta.content.decode()
    assert "A largo plazo, el espacio estará Medio el 38.89 % del tiempo" in (
        respuesta.content.decode()
    )


@pytest.mark.parametrize("estado_inicial", ["no-es-entero", "99", "-1"])
def test_estado_inicial_invalido_usa_cero_y_muestra_aviso(client, estado_inicial):
    """Un estado inicial inválido usa el primer estado y avisa al usuario."""
    escenario = Escenario.objects.get(nombre="Salón 101")
    respuesta = client.get(
        reverse("ocupacion:detalle", args=[escenario.pk]),
        {"estado_inicial": estado_inicial},
    )

    assert respuesta.status_code == 200
    assert respuesta.context["indice_estado_inicial"] == 0
    assert respuesta.context["aviso_estado_invalido"]
    assert "no es válido" in respuesta.content.decode()
    evolucion = extraer_json_script(respuesta, "datos-evolucion")
    assert evolucion[0] == [1, 0, 0]
