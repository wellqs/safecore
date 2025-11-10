from django.contrib import admin
from .models import Relatorio, RelatorioAtividade


class RelatorioAtividadeInline(admin.TabularInline):
    model = RelatorioAtividade
    extra = 0
    fields = ("ordem", "nome", "contador")
    readonly_fields = ("nome",)


@admin.register(Relatorio)
class RelatorioAdmin(admin.ModelAdmin):
    list_display = ("titulo", "categoria", "data", "criado_em")
    list_filter = ("categoria", "data")
    inlines = [RelatorioAtividadeInline]

