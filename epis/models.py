from django.db import models
from hr.models import Vinculo
from pgr.models import Risco
from org.models import Funcao


class EPI(models.Model):
    nome = models.CharField(max_length=150)
    numero_ca = models.CharField("Número CA", max_length=30, unique=True)
    validade_ca = models.DateField("Validade do CA", null=True, blank=True)
    fabricante = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        verbose_name = "EPI"
        verbose_name_plural = "EPIs"

    def __str__(self) -> str:
        return f"{self.nome} (CA {self.numero_ca})"


class EPIRequisito(models.Model):
    funcao = models.ForeignKey(Funcao, on_delete=models.CASCADE, related_name="epis_requisitos")
    risco = models.ForeignKey(Risco, on_delete=models.CASCADE, related_name="epis_requisitos")
    epi = models.ForeignKey(EPI, on_delete=models.CASCADE, related_name="requisitos")

    class Meta:
        verbose_name = "Requisito de EPI"
        verbose_name_plural = "Requisitos de EPI"
        constraints = [
            models.UniqueConstraint(fields=["funcao", "risco", "epi"], name="unique_epi_requisito")
        ]


class EntregaEPI(models.Model):
    vinculo = models.ForeignKey(Vinculo, on_delete=models.CASCADE, related_name="entregas_epi")
    epi = models.ForeignKey(EPI, on_delete=models.PROTECT, related_name="entregas")
    quantidade = models.PositiveIntegerField(default=1)
    entregue_em = models.DateField(auto_now_add=True)
    aceite_digital = models.BooleanField(default=False)
    aceite_em = models.DateTimeField(null=True, blank=True)
    observacao = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Entrega de EPI"
        verbose_name_plural = "Entregas de EPI"

