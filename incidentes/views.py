from django.views.generic import ListView
from . import models


class IncidenteListView(ListView):
    model = models.Incidente
    template_name = "incidentes/incidentes.html"


class AcaoListView(ListView):
    model = models.Acao
    template_name = "incidentes/acoes.html"

