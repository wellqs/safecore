from django.views.generic import ListView
from . import models


class NotificacaoListView(ListView):
    model = models.Notificacao
    template_name = "notificacoes/notificacoes.html"

