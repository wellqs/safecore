from django.contrib import admin
from . import models


@admin.register(models.Checklist)
class ChecklistAdmin(admin.ModelAdmin):
    list_display = ("nome", "unidade", "setor", "ativo")
    list_filter = ("ativo", "unidade", "setor")


@admin.register(models.ChecklistItem)
class ChecklistItemAdmin(admin.ModelAdmin):
    list_display = ("checklist", "texto")


@admin.register(models.Inspecao)
class InspecaoAdmin(admin.ModelAdmin):
    list_display = ("checklist", "responsavel", "status", "realizada_em")
    list_filter = ("status",)


@admin.register(models.InspecaoResposta)
class InspecaoRespostaAdmin(admin.ModelAdmin):
    list_display = ("inspecao", "item", "conforme")


@admin.register(models.NaoConformidade)
class NaoConformidadeAdmin(admin.ModelAdmin):
    list_display = ("inspecao", "responsavel", "status", "prazo")
    list_filter = ("status",)

