from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

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
