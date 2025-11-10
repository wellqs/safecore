from django.urls import path
from . import views

app_name = "pgr"

urlpatterns = [
    path("riscos/", views.RiscoListView.as_view(), name="riscos"),
    path("mapas/", views.MapaExposicaoListView.as_view(), name="mapas"),
    path("exposicoes/", views.ExposicaoListView.as_view(), name="exposicoes"),
    path("relatorio/pdf/", views.exportar_relatorio_pdf, name="relatorio_pdf"),
]
