from django.db import models
from org.models import Funcao, AmbienteTrabalho
from hr.models import Vinculo


class TipoRisco(models.TextChoices):
    FISICO = "FIS", "Físico"
    QUIMICO = "QUI", "Químico"
    BIOLOGICO = "BIO", "Biológico"
    ERGONOMICO = "ERG", "Ergonômico"
    ACIDENTE = "ACI", "Acidente/Mecânico"


class Risco(models.Model):
    codigo_esocial = models.CharField("Código eSocial", max_length=10, unique=True)
    nome = models.CharField("Nome do Risco", max_length=200)
    tipo = models.CharField("Tipo do Risco", max_length=3, choices=TipoRisco.choices)
    descricao = models.TextField("Descrição", blank=True, null=True)

    class Meta:
        verbose_name = "Risco"
        verbose_name_plural = "Riscos (Tab. 24)"

    def __str__(self) -> str:
        return f"{self.codigo_esocial} - {self.nome}"


class Inventario(models.Model):
    criado_em = models.DateTimeField(auto_now_add=True)
    descricao = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Inventário de Perigos e Riscos"
        verbose_name_plural = "Inventários de Perigos e Riscos"


class Exposicao(models.Model):
    vinculo = models.ForeignKey(Vinculo, on_delete=models.CASCADE, related_name="exposicoes")
    funcao = models.ForeignKey(Funcao, on_delete=models.PROTECT, related_name="exposicoes")
    ambiente = models.ForeignKey(AmbienteTrabalho, on_delete=models.PROTECT, related_name="exposicoes")
    risco = models.ForeignKey(Risco, on_delete=models.PROTECT, related_name="exposicoes")

    probabilidade = models.PositiveSmallIntegerField(default=1)
    severidade = models.PositiveSmallIntegerField(default=1)
    intensidade = models.CharField(max_length=100, blank=True, null=True)
    tecnica_utilizada = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = "Exposição a Risco"
        verbose_name_plural = "Exposições a Riscos"
        constraints = [
            models.UniqueConstraint(fields=["vinculo", "ambiente", "risco"], name="unique_exposicao_vinculo")
        ]

    @property
    def risco_score(self) -> int:
        return int(self.probabilidade) * int(self.severidade)


class MedidaControle(models.Model):
    class Tipo(models.TextChoices):
        ELIMINACAO = "ELI", "Eliminação"
        SUBSTITUICAO = "SUB", "Substituição"
        EPC = "EPC", "Proteção Coletiva"
        ADMINISTRATIVA = "ADM", "Administrativa"
        EPI = "EPI", "Proteção Individual"

    risco = models.ForeignKey(Risco, on_delete=models.CASCADE, related_name="medidas")
    descricao = models.CharField(max_length=255)
    tipo = models.CharField(max_length=3, choices=Tipo.choices)

    class Meta:
        verbose_name = "Medida de Controle"
        verbose_name_plural = "Medidas de Controle"


class MapaExposicao(models.Model):
    funcao = models.ForeignKey(Funcao, on_delete=models.CASCADE, related_name="mapas_exposicao")
    ambiente = models.ForeignKey(AmbienteTrabalho, on_delete=models.CASCADE, related_name="mapas_exposicao")
    risco = models.ForeignKey(Risco, on_delete=models.PROTECT, related_name="mapas_exposicao")
    intensidade = models.CharField(max_length=100, blank=True, null=True)
    tecnica_utilizada = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = "Mapa de Exposição (Função/Ambiente)"
        verbose_name_plural = "Mapas de Exposição (Função/Ambiente)"
        constraints = [
            models.UniqueConstraint(fields=["funcao", "ambiente", "risco"], name="unique_mapa_exposicao")
        ]
