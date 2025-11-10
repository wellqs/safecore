from django.views.generic import ListView
from . import models


class ChecklistListView(ListView):
    model = models.Checklist
    template_name = "inspecoes/checklists.html"


class InspecaoListView(ListView):
    model = models.Inspecao
    template_name = "inspecoes/inspecoes.html"


class NCListView(ListView):
    model = models.NaoConformidade
    template_name = "inspecoes/ncs.html"

