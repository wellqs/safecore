from django.views.generic import ListView
from . import models


class TreinamentoListView(ListView):
    model = models.Treinamento
    template_name = "treinamentos/treinamentos.html"


class MatriculaListView(ListView):
    model = models.Matricula
    template_name = "treinamentos/matriculas.html"

