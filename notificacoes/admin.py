from django.contrib import admin
from . import models


@admin.register(models.Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "canal", "destino", "disparada_em", "lida")
    list_filter = ("canal", "lida")

