from django.db import models
from org.models import Unidade, Setor


class Checklist(models.Model):
    nome = models.CharField(max_length=150)
    descricao = models.TextField(blank=True, null=True)
    unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE, related_name="checklists")
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE, related_name="checklists")
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Checklist"
        verbose_name_plural = "Checklists"
        unique_together = ("setor", "nome")

    def __str__(self) -> str:
        return self.nome


class ChecklistItem(models.Model):
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE, related_name="itens")
    texto = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Item do Checklist"
        verbose_name_plural = "Itens do Checklist"

    def __str__(self) -> str:
        return self.texto


class Inspecao(models.Model):
    class Status(models.TextChoices):
        ABERTA = "ABE", "Aberta"
        EM_ANDAMENTO = "AND", "Em andamento"
        CONCLUIDA = "CON", "Concluída"

    checklist = models.ForeignKey(Checklist, on_delete=models.PROTECT, related_name="inspecoes")
    realizada_em = models.DateTimeField(auto_now_add=True)
    responsavel = models.CharField(max_length=150)
    status = models.CharField(max_length=3, choices=Status.choices, default=Status.ABERTA)

    class Meta:
        verbose_name = "Inspeção"
        verbose_name_plural = "Inspeções"


class InspecaoResposta(models.Model):
    inspecao = models.ForeignKey(Inspecao, on_delete=models.CASCADE, related_name="respostas")
    item = models.ForeignKey(ChecklistItem, on_delete=models.PROTECT)
    conforme = models.BooleanField(null=True)
    observacao = models.CharField(max_length=255, blank=True, null=True)
    foto = models.FileField(upload_to="inspecoes/fotos/", blank=True, null=True)

    class Meta:
        verbose_name = "Resposta da Inspeção"
        verbose_name_plural = "Respostas de Inspeção"


class NaoConformidade(models.Model):
    inspecao = models.ForeignKey(Inspecao, on_delete=models.CASCADE, related_name="nao_conformidades")
    descricao = models.CharField(max_length=255)
    responsavel = models.CharField(max_length=150)
    prazo = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, default="aberta")

    class Meta:
        verbose_name = "Não Conformidade"
        verbose_name_plural = "Não Conformidades"

