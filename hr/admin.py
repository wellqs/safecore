from django.contrib import admin
from . import models


@admin.register(models.Colaborador)
class ColaboradorAdmin(admin.ModelAdmin):
    list_display = ("nome_completo", "cpf", "empresa")
    search_fields = ("nome_completo", "cpf")
    list_filter = ("empresa",)


@admin.register(models.Vinculo)
class VinculoAdmin(admin.ModelAdmin):
    list_display = ("colaborador", "funcao", "unidade", "setor", "data_admissao", "ativo")
    list_filter = ("ativo", "unidade", "setor")
    search_fields = ("colaborador__nome_completo", "funcao__nome")

