from django.db import models
from hr.models import Vinculo


class Treinamento(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nome = models.CharField(max_length=200)
    nr = models.CharField("NR", max_length=10, blank=True, null=True)
    validade_meses = models.PositiveIntegerField(default=12)

    class Meta:
        verbose_name = "Treinamento"
        verbose_name_plural = "Treinamentos"

    def __str__(self) -> str:
        return f"{self.codigo} - {self.nome}"


class Matricula(models.Model):
    class Status(models.TextChoices):
        MATRICULADO = "MAT", "Matriculado"
        CONCLUIDO = "CON", "Concluído"
        VENCIDO = "VEN", "Vencido"

    vinculo = models.ForeignKey(Vinculo, on_delete=models.CASCADE, related_name="matriculas")
    treinamento = models.ForeignKey(Treinamento, on_delete=models.CASCADE, related_name="matriculas")
    data_inicio = models.DateField()
    data_conclusao = models.DateField(null=True, blank=True)
    validade_ate = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=3, choices=Status.choices, default=Status.MATRICULADO)

    class Meta:
        verbose_name = "Matrícula"
        verbose_name_plural = "Matrículas"
        constraints = [
            models.UniqueConstraint(fields=["vinculo", "treinamento", "data_inicio"], name="unique_matricula_inicio")
        ]

