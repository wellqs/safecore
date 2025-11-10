from django.views.generic import ListView
from . import models


class EmpresaListView(ListView):
    model = models.Empresa
    template_name = "org/empresas.html"


class UnidadeListView(ListView):
    model = models.Unidade
    template_name = "org/unidades.html"


class SetorListView(ListView):
    model = models.Setor
    template_name = "org/setores.html"


class FuncaoListView(ListView):
    model = models.Funcao
    template_name = "org/funcoes.html"


class AmbienteListView(ListView):
    model = models.AmbienteTrabalho
    template_name = "org/ambientes.html"

