from django.views.generic import ListView
from . import models


class ColaboradorListView(ListView):
    model = models.Colaborador
    template_name = "hr/colaboradores.html"


class VinculoListView(ListView):
    model = models.Vinculo
    template_name = "hr/vinculos.html"

