# safecore/core/admin.py

from django.contrib import admin
from .models import (
    Empresa, Cargo, Funcionario, AmbienteDeTrabalho, Risco,
    ExposicaoRisco, Exame, Aso
)

# --- BASE ---

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('razao_social', 'cnpj')
    search_fields = ('razao_social', 'cnpj')

@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'cpf', 'empresa', 'cargo', 'data_admissao')
    list_filter = ('empresa', 'cargo')
    search_fields = ('nome_completo', 'cpf')
    autocomplete_fields = ('empresa', 'cargo')

# --- PGR ---

@admin.register(AmbienteDeTrabalho)
class AmbienteDeTrabalhoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'empresa')
    list_filter = ('empresa',)
    search_fields = ('nome',)
    autocomplete_fields = ('empresa',)

@admin.register(Risco)
class RiscoAdmin(admin.ModelAdmin):
    list_display = ('codigo_esocial', 'nome', 'get_tipo_display')
    list_filter = ('tipo',)
    search_fields = ('codigo_esocial', 'nome')

@admin.register(ExposicaoRisco)
class ExposicaoRiscoAdmin(admin.ModelAdmin):
    list_display = ('cargo', 'ambiente', 'risco')
    list_filter = ('ambiente__empresa', 'cargo', 'risco__tipo')
    search_fields = ('cargo__nome', 'ambiente__nome', 'risco__nome')
    autocomplete_fields = ['cargo', 'ambiente', 'risco']

# --- PCMSO ---

@admin.register(Exame)
class ExameAdmin(admin.ModelAdmin):
    list_display = ('codigo_esocial', 'nome')
    search_fields = ('codigo_esocial', 'nome')

@admin.register(Aso)
class AsoAdmin(admin.ModelAdmin):
    list_display = ('funcionario', 'get_tipo_display', 'get_resultado_display', 'data_exame', 'vencimento')
    list_filter = ('tipo', 'resultado', 'funcionario__empresa')
    search_fields = ('funcionario__nome_completo', 'funcionario__cpf')
    autocomplete_fields = ('funcionario',)
    filter_horizontal = ('exames_realizados',) # Melhora a UI para ManyToManyToMany