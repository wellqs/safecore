from django.views.generic import ListView
from . import models


class EPIListView(ListView):
    model = models.EPI
    template_name = "epis/epis.html"


class RequisitoListView(ListView):
    model = models.EPIRequisito
    template_name = "epis/requisitos.html"


class EntregaListView(ListView):
    model = models.EntregaEPI
    template_name = "epis/entregas.html"

