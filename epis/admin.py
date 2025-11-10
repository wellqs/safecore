from django.contrib import admin
from . import models


@admin.register(models.EPI)
class EPIAdmin(admin.ModelAdmin):
    list_display = ("nome", "numero_ca", "validade_ca")
    search_fields = ("nome", "numero_ca")


@admin.register(models.EPIRequisito)
class EPIRequisitoAdmin(admin.ModelAdmin):
    list_display = ("funcao", "risco", "epi")
    list_filter = ("funcao", "risco")


@admin.register(models.EntregaEPI)
class EntregaEPIAdmin(admin.ModelAdmin):
    list_display = ("vinculo", "epi", "quantidade", "entregue_em", "aceite_digital")
    list_filter = ("aceite_digital",)

