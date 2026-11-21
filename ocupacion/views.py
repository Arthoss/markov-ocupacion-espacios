from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from markov.core import distribucion_estacionaria, evolucion, predecir_pasos

from .forms import EscenarioForm
from .models import Escenario


class EscenarioListView(ListView):
    model = Escenario
    template_name = "ocupacion/escenario_list.html"
    context_object_name = "escenarios"


class EscenarioCreateView(CreateView):
    model = Escenario
    form_class = EscenarioForm
    template_name = "ocupacion/escenario_form.html"

    def get_success_url(self):
        return reverse_lazy("ocupacion:detalle", kwargs={"pk": self.object.pk})


class EscenarioDetailView(DetailView):
    model = Escenario
    template_name = "ocupacion/escenario_detail.html"
    context_object_name = "escenario"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        estados = self.object.estados
        cantidad_estados = len(estados)
        valor_estado = self.request.GET.get("estado_inicial")
        aviso_estado = False

        if valor_estado is None:
            indice_estado = 0
        else:
            try:
                indice_estado = int(valor_estado)
            except (TypeError, ValueError):
                indice_estado = 0
                aviso_estado = True
            else:
                if not 0 <= indice_estado < cantidad_estados:
                    indice_estado = 0
                    aviso_estado = True

        vector_inicial = [0] * cantidad_estados
        vector_inicial[indice_estado] = 1
        predicciones = predecir_pasos(self.object.matriz, vector_inicial)
        pasos_referencia = (1, 3, 5, 10)
        resultados = [
            {
                "paso": paso,
                "valores": [
                    f"{probabilidad * 100:.2f} %"
                    for probabilidad in predicciones[paso]
                ],
            }
            for paso in pasos_referencia
        ]
        filas_matriz = [
            {"estado": estado, "valores": fila}
            for estado, fila in zip(estados, self.object.matriz)
        ]
        estacionaria = distribucion_estacionaria(self.object.matriz)
        indice_mas_probable = max(
            range(cantidad_estados), key=lambda indice: estacionaria[indice]
        )
        evolucion_datos = evolucion(self.object.matriz, vector_inicial, hasta=10)

        contexto.update(
            {
                "indice_estado_inicial": indice_estado,
                "aviso_estado_invalido": aviso_estado,
                "filas_matriz": filas_matriz,
                "resultados": resultados,
                "resultados_estacionarios": [
                    {
                        "estado": estado,
                        "valor": f"{probabilidad * 100:.2f} %",
                        "es_mas_probable": indice == indice_mas_probable,
                    }
                    for indice, (estado, probabilidad) in enumerate(
                        zip(estados, estacionaria)
                    )
                ],
                "indice_estado_mas_probable": indice_mas_probable,
                "estado_mas_probable": estados[indice_mas_probable],
                "interpretacion_estacionaria": (
                    f"A largo plazo, el espacio estará {estados[indice_mas_probable]} "
                    f"el {estacionaria[indice_mas_probable] * 100:.2f} % del tiempo"
                ),
                "datos_estados_json": estados,
                "datos_evolucion_json": evolucion_datos,
                "datos_predicciones_json": {
                    paso: predicciones[paso] for paso in pasos_referencia
                },
            }
        )
        return contexto


class EscenarioUpdateView(UpdateView):
    model = Escenario
    form_class = EscenarioForm
    template_name = "ocupacion/escenario_form.html"

    def get_success_url(self):
        return reverse_lazy("ocupacion:detalle", kwargs={"pk": self.object.pk})


class EscenarioDeleteView(DeleteView):
    model = Escenario
    template_name = "ocupacion/escenario_confirm_delete.html"
    context_object_name = "escenario"
    success_url = reverse_lazy("ocupacion:lista")
