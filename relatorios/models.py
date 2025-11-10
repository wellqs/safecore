from django.db import models


class Relatorio(models.Model):
    class Categoria(models.TextChoices):
        SEGURANCA = "SEG", "Segurança do Trabalho"
        SAUDE = "SAU", "Saúde do Trabalhador"

    titulo = models.CharField(max_length=200)
    categoria = models.CharField(max_length=3, choices=Categoria.choices)
    data = models.DateField()
    observacao = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Relatório"
        verbose_name_plural = "Relatórios"
        ordering = ("-data", "-criado_em")

    def __str__(self) -> str:
        return f"{self.get_categoria_display()} - {self.titulo} ({self.data})"


class RelatorioAtividade(models.Model):
    relatorio = models.ForeignKey(Relatorio, on_delete=models.CASCADE, related_name="atividades")
    nome = models.CharField(max_length=255)
    contador = models.PositiveIntegerField(default=0)
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Atividade do Relatório"
        verbose_name_plural = "Atividades do Relatório"
        ordering = ("ordem", "id")

