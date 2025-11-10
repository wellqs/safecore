from django.urls import path
from . import views

app_name = "incidentes"

urlpatterns = [
    path("incidentes/", views.IncidenteListView.as_view(), name="incidentes"),
    path("acoes/", views.AcaoListView.as_view(), name="acoes"),
]

