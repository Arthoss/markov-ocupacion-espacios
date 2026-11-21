import re

from django import forms
from django.core.exceptions import ValidationError

from markov.core import MatrizInvalidaError, validar_matriz

from .models import Escenario


class EscenarioForm(forms.ModelForm):
    estados = forms.CharField(
        label="Estados",
        help_text="Escribe los nombres de los estados separados por comas.",
        widget=forms.TextInput,
    )
    matriz = forms.CharField(
        label="Matriz de transición",
        help_text=(
            "Escribe una fila por línea, con valores separados por espacios o comas. "
            "Usa punto para los decimales."
        ),
        widget=forms.Textarea,
    )

    class Meta:
        model = Escenario
        fields = ["nombre", "estados", "matriz"]

    def __init__(self, *args, **kwargs):
        initial_provided = kwargs.get("initial", {})
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            if "estados" not in initial_provided:
                self.initial["estados"] = ", ".join(self.instance.estados)
            if "matriz" not in initial_provided:
                self.initial["matriz"] = "\n".join(
                    " ".join(f"{valor:.2f}" for valor in fila)
                    for fila in self.instance.matriz
                )

    def clean_estados(self):
        return [estado.strip() for estado in self.cleaned_data["estados"].split(",")]

    def clean_matriz(self):
        texto = self.cleaned_data["matriz"]
        matriz = []
        try:
            for linea in texto.splitlines():
                if not linea.strip():
                    continue
                matriz.append(
                    [float(valor) for valor in re.split(r"[\s,]+", linea.strip())]
                )
        except ValueError as error:
            raise ValidationError(
                "La matriz debe usar números válidos y punto para los decimales."
            ) from error
        return matriz

    def clean(self):
        datos = super().clean()
        estados = datos.get("estados")
        matriz = datos.get("matriz")
        if estados is None or matriz is None:
            return datos

        if len(estados) < 3:
            self.add_error("estados", "Se requieren mínimo 3 estados.")
            return datos
        if any(not estado for estado in estados):
            self.add_error("estados", "Los nombres de los estados no pueden estar vacíos.")
            return datos
        estados_normalizados = [estado.casefold() for estado in estados]
        if len(set(estados_normalizados)) != len(estados_normalizados):
            self.add_error("estados", "Los nombres de los estados deben ser únicos.")
            return datos
        if len(matriz) != len(estados):
            self.add_error("matriz", "La matriz debe tener una fila por cada estado.")
            return datos
        if any(len(fila) != len(estados) for fila in matriz):
            self.add_error("matriz", "La matriz debe tener una columna por cada estado.")
            return datos

        try:
            validar_matriz(matriz)
        except MatrizInvalidaError as error:
            self.add_error("matriz", str(error))
        return datos
