from django.db import models
from org.models import Unidade


class Incidente(models.Model):
    class Gravidade(models.TextChoices):
        LEVE = "LEV", "Leve"
        MODERADA = "MOD", "Moderada"
        GRAVE = "GRA", "Grave"

    unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE, related_name="incidentes")
    data = models.DateTimeField()
    tipo = models.CharField(max_length=100)
    gravidade = models.CharField(max_length=3, choices=Gravidade.choices)
    local = models.CharField(max_length=150)
    descricao = models.TextField()

    class Meta:
        verbose_name = "Incidente/Acidente"
        verbose_name_plural = "Incidentes/Acidentes"
        ordering = ("-data",)


class Investigacao(models.Model):
    incidente = models.OneToOneField(Incidente, on_delete=models.CASCADE, related_name="investigacao")
    cinco_porques = models.TextField(blank=True, null=True)
    arvore_causas = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Investigação"
        verbose_name_plural = "Investigações"


class Acao(models.Model):
    incidente = models.ForeignKey(Incidente, on_delete=models.CASCADE, related_name="acoes")
    descricao = models.CharField(max_length=255)
    responsavel = models.CharField(max_length=150)
    prazo = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, default="aberta")

    class Meta:
        verbose_name = "Ação do Incidente"
        verbose_name_plural = "Ações do Incidente"

