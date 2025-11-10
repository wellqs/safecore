from django.contrib import admin
from . import models


@admin.register(models.Risco)
class RiscoAdmin(admin.ModelAdmin):
    list_display = ("codigo_esocial", "nome", "tipo")
    search_fields = ("codigo_esocial", "nome")
    list_filter = ("tipo",)


@admin.register(models.Exposicao)
class ExposicaoAdmin(admin.ModelAdmin):
    list_display = ("vinculo", "funcao", "ambiente", "risco", "probabilidade", "severidade")
    list_filter = ("ambiente", "risco")
    search_fields = ("vinculo__colaborador__nome_completo", "funcao__nome", "risco__nome")


@admin.register(models.MedidaControle)
class MedidaControleAdmin(admin.ModelAdmin):
    list_display = ("risco", "tipo", "descricao")
    list_filter = ("tipo",)


@admin.register(models.MapaExposicao)
class MapaExposicaoAdmin(admin.ModelAdmin):
    list_display = ("funcao", "ambiente", "risco", "intensidade")
    list_filter = ("ambiente", "risco")
