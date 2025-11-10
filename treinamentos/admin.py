from django.contrib import admin
from . import models


@admin.register(models.Treinamento)
class TreinamentoAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nome", "nr", "validade_meses")
    search_fields = ("codigo", "nome", "nr")


@admin.register(models.Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ("vinculo", "treinamento", "status", "data_inicio", "validade_ate")
    list_filter = ("status",)

