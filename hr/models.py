from django.db import models
from org.models import Empresa, Unidade, Setor, Funcao


class Colaborador(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="colaboradores")
    nome_completo = models.CharField(max_length=200)
    cpf = models.CharField(max_length=14, unique=True)
    data_nascimento = models.DateField(null=True, blank=True)
    pis = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.nome_completo} ({self.cpf})"

    class Meta:
        verbose_name = "Colaborador"
        verbose_name_plural = "Colaboradores"


class Vinculo(models.Model):
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE, related_name="vinculos")
    funcao = models.ForeignKey(Funcao, on_delete=models.PROTECT, related_name="vinculos")
    unidade = models.ForeignKey(Unidade, on_delete=models.PROTECT, related_name="vinculos")
    setor = models.ForeignKey(Setor, on_delete=models.PROTECT, related_name="vinculos")
    data_admissao = models.DateField()
    data_demissao = models.DateField(null=True, blank=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Vínculo"
        verbose_name_plural = "Vínculos"
        ordering = ("-ativo", "-data_admissao")
        constraints = [
            models.UniqueConstraint(fields=["colaborador", "funcao", "unidade", "setor", "data_admissao"], name="unique_vinculo_inicio")
        ]

    def __str__(self) -> str:
        return f"{self.colaborador} - {self.funcao} ({'ativo' if self.ativo else 'inativo'})"

