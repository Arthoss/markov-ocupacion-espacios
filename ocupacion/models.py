from django.core.exceptions import ValidationError
from django.db import models

from markov.core import MatrizInvalidaError, validar_matriz


class Escenario(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    estados = models.JSONField()
    matriz = models.JSONField()
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

    def clean(self):
        super().clean()
        errores = {}

        if not isinstance(self.estados, list):
            errores["estados"] = "Los estados deben ser una lista."
        else:
            estados_normalizados = [
                estado.strip().casefold() if isinstance(estado, str) else ""
                for estado in self.estados
            ]
            if len(estados_normalizados) < 3:
                errores["estados"] = "Se requieren mínimo 3 estados."
            elif any(not estado for estado in estados_normalizados):
                errores["estados"] = "Los nombres de los estados no pueden estar vacíos."
            elif len(set(estados_normalizados)) != len(estados_normalizados):
                errores["estados"] = "Los nombres de los estados deben ser únicos."

        if errores:
            raise ValidationError(errores)

        if not isinstance(self.matriz, list) or len(self.matriz) != len(self.estados):
            raise ValidationError(
                {"matriz": "La matriz debe tener una fila por cada estado."}
            )
        if any(
            not isinstance(fila, list) or len(fila) != len(self.estados)
            for fila in self.matriz
        ):
            raise ValidationError(
                {"matriz": "La matriz debe tener una columna por cada estado."}
            )

        try:
            validar_matriz(self.matriz)
        except MatrizInvalidaError as error:
            raise ValidationError({"matriz": str(error)}) from error
