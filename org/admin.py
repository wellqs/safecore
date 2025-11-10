from django.contrib import admin
from . import models


@admin.register(models.Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ("razao_social", "cnpj", "nome_fantasia")
    search_fields = ("razao_social", "cnpj", "nome_fantasia")


@admin.register(models.Unidade)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ("nome", "empresa", "cnpj")
    search_fields = ("nome", "cnpj", "empresa__razao_social")
    list_filter = ("empresa",)


@admin.register(models.Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ("nome", "unidade")
    list_filter = ("unidade",)
    search_fields = ("nome", "unidade__nome")


@admin.register(models.Funcao)
class FuncaoAdmin(admin.ModelAdmin):
    list_display = ("nome", "setor")
    list_filter = ("setor__unidade", "setor")
    search_fields = ("nome",)


@admin.register(models.AmbienteTrabalho)
class AmbienteTrabalhoAdmin(admin.ModelAdmin):
    list_display = ("nome", "unidade")
    list_filter = ("unidade",)
    search_fields = ("nome",)

