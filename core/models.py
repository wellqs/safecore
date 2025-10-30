# safecore/core/models.py

from django.db import models
from django.utils import timezone  # Importado para usar a data atual


# ==============================================================================
# BASE MODELS (Empresa, Cargo, Funcionário)
# ==============================================================================

class Empresa(models.Model):
    razao_social = models.CharField("Razão Social", max_length=200)
    nome_fantasia = models.CharField("Nome Fantasia", max_length=200, blank=True, null=True)
    cnpj = models.CharField("CNPJ", max_length=18, unique=True)

    # Adicione outros campos como endereço, telefone, etc. conforme necessário

    def __str__(self):
        return f"{self.razao_social} ({self.cnpj})"

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"


class Cargo(models.Model):
    nome = models.CharField("Nome do Cargo", max_length=100, unique=True)
    descricao = models.TextField("Descrição das Atividades", blank=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"


class Funcionario(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name="Empresa")
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT, verbose_name="Cargo")
    nome_completo = models.CharField("Nome Completo", max_length=200)
    cpf = models.CharField("CPF", max_length=14, unique=True)
    data_admissao = models.DateField("Data de Admissão")

    # Adicione data de nascimento, PIS, etc. conforme necessário

    def __str__(self):
        return f"{self.nome_completo} ({self.cpf})"

    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"


# ==============================================================================
# MODELOS DE GESTÃO DE RISCOS (PGR) - Base para eSocial S-2240
# ==============================================================================

class AmbienteDeTrabalho(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name="Empresa")
    nome = models.CharField("Nome do Ambiente", max_length=150)
    descricao = models.TextField("Descrição do Ambiente", blank=True, null=True)

    def __str__(self):
        return f"{self.nome} ({self.empresa.nome_fantasia or self.empresa.razao_social})"

    class Meta:
        verbose_name = "Ambiente de Trabalho"
        verbose_name_plural = "Ambientes de Trabalho"
        unique_together = ('empresa', 'nome')  # Garante que não haja ambientes com o mesmo nome na mesma empresa


class TipoRisco(models.TextChoices):
    FISICO = 'FIS', 'Físico'
    QUIMICO = 'QUI', 'Químico'
    BIOLOGICO = 'BIO', 'Biológico'
    ERGONOMICO = 'ERG', 'Ergonômico'
    ACIDENTES = 'ACI', 'Acidentes/Mecânico'


class Risco(models.Model):
    # Tabela 24 do eSocial
    codigo_esocial = models.CharField("Código eSocial", max_length=10, unique=True,
                                      help_text="Código correspondente à Tabela 24 do eSocial.")
    nome = models.CharField("Nome do Risco", max_length=200)
    tipo = models.CharField("Tipo do Risco", max_length=3, choices=TipoRisco.choices)
    descricao = models.TextField("Descrição do Risco/Fonte Geradora", blank=True, null=True)

    def __str__(self):
        return f"{self.codigo_esocial} - {self.nome}"

    class Meta:
        verbose_name = "Risco"
        verbose_name_plural = "Riscos (Tabela 24)"


class ExposicaoRisco(models.Model):
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, verbose_name="Cargo")
    ambiente = models.ForeignKey(AmbienteDeTrabalho, on_delete=models.CASCADE, verbose_name="Ambiente de Trabalho")
    risco = models.ForeignKey(Risco, on_delete=models.PROTECT, verbose_name="Risco")

    # Campos alinhados com o evento S-2240 do eSocial
    intensidade = models.CharField("Intensidade/Concentração", max_length=100, blank=True, null=True)
    tecnica_utilizada = models.CharField("Técnica Utilizada para Medição", max_length=200, blank=True, null=True)

    # Adicione campos para EPC e EPI conforme a evolução do projeto

    def __str__(self):
        return f"{self.cargo} em {self.ambiente} -> {self.risco}"

    class Meta:
        verbose_name = "Exposição de Risco"
        verbose_name_plural = "Exposições de Riscos"
        # Garante que a mesma combinação de cargo, ambiente e risco não seja cadastrada duas vezes
        constraints = [
            models.UniqueConstraint(fields=['cargo', 'ambiente', 'risco'], name='unique_exposicao_risco')
        ]


# ==============================================================================
# MODELOS DE SAÚDE OCUPACIONAL (PCMSO) - Base para eSocial S-2220
# ==============================================================================

class Exame(models.Model):
    # Tabela 27 do eSocial
    codigo_esocial = models.CharField("Código eSocial", max_length=10, unique=True,
                                      help_text="Código correspondente à Tabela 27 do eSocial.")
    nome = models.CharField("Nome do Procedimento Diagnóstico", max_length=200)
    descricao = models.TextField("Descrição", blank=True, null=True)

    def __str__(self):
        return f"{self.codigo_esocial} - {self.nome}"

    class Meta:
        verbose_name = "Exame"
        verbose_name_plural = "Exames (Tabela 27)"


class Aso(models.Model):
    class TipoAso(models.TextChoices):
        ADMISSIONAL = 'ADM', 'Admissional'
        PERIODICO = 'PER', 'Periódico'
        RETORNO = 'RET', 'Retorno ao Trabalho'
        MUDANCA = 'MUD', 'Mudança de Risco Ocupacional'
        DEMISSIONAL = 'DEM', 'Demissional'

    class ResultadoAso(models.TextChoices):
        APTO = 'AP', 'Apto'
        INAPTO = 'IN', 'Inapto'

    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, verbose_name="Funcionário")
    tipo = models.CharField("Tipo de ASO", max_length=3, choices=TipoAso.choices)
    resultado = models.CharField("Resultado", max_length=2, choices=ResultadoAso.choices)
    data_exame = models.DateField("Data do Exame", default=timezone.now)
    vencimento = models.DateField("Data de Vencimento", blank=True, null=True)

    exames_realizados = models.ManyToManyField(Exame, verbose_name="Exames Realizados")

    medico_responsavel_nome = models.CharField("Nome do Médico Responsável", max_length=200)
    medico_responsavel_crm = models.CharField("CRM do Médico Responsável", max_length=20)

    def __str__(self):
        # O .get_tipo_display() pega o nome amigável da escolha (ex: "Admissional")
        return f"ASO {self.get_tipo_display()} de {self.funcionario.nome_completo} em {self.data_exame.strftime('%d/%m/%Y')}"

    class Meta:
        verbose_name = "ASO - Atestado de Saúde Ocupacional"
        verbose_name_plural = "ASOs - Atestados de Saúde Ocupacional"
        ordering = ['-data_exame']