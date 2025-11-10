from django.urls import path
from . import views

app_name = "org"

urlpatterns = [
    path("empresas/", views.EmpresaListView.as_view(), name="empresas"),
    path("unidades/", views.UnidadeListView.as_view(), name="unidades"),
    path("setores/", views.SetorListView.as_view(), name="setores"),
    path("funcoes/", views.FuncaoListView.as_view(), name="funcoes"),
    path("ambientes/", views.AmbienteListView.as_view(), name="ambientes"),
]

