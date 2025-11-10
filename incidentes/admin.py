from django.contrib import admin
from . import models


@admin.register(models.Incidente)
class IncidenteAdmin(admin.ModelAdmin):
    list_display = ("unidade", "data", "tipo", "gravidade", "local")
    list_filter = ("gravidade", "unidade")


@admin.register(models.Investigacao)
class InvestigacaoAdmin(admin.ModelAdmin):
    list_display = ("incidente",)


@admin.register(models.Acao)
class AcaoAdmin(admin.ModelAdmin):
    list_display = ("incidente", "responsavel", "status", "prazo")
    list_filter = ("status",)

