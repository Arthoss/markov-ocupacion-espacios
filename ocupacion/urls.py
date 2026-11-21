from django.urls import path

from . import views

app_name = "ocupacion"

urlpatterns = [
    path("", views.EscenarioListView.as_view(), name="lista"),
    path("escenarios/nuevo/", views.EscenarioCreateView.as_view(), name="crear"),
    path("escenarios/<int:pk>/", views.EscenarioDetailView.as_view(), name="detalle"),
    path(
        "escenarios/<int:pk>/editar/",
        views.EscenarioUpdateView.as_view(),
        name="editar",
    ),
    path(
        "escenarios/<int:pk>/eliminar/",
        views.EscenarioDeleteView.as_view(),
        name="eliminar",
    ),
]
