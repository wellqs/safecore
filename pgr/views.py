from django.views.generic import ListView
from django.http import HttpResponse
from . import models


class RiscoListView(ListView):
    model = models.Risco
    template_name = "pgr/riscos.html"


class MapaExposicaoListView(ListView):
    model = models.MapaExposicao
    template_name = "pgr/mapas.html"


class ExposicaoListView(ListView):
    model = models.Exposicao
    template_name = "pgr/exposicoes.html"


def exportar_relatorio_pdf(request):
    # Placeholder de exportação. Integração com WeasyPrint/ReportLab virá depois.
    return HttpResponse("Relatório PGR (PDF) - em breve.", content_type="text/plain")
