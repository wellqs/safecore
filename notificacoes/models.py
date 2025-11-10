from django.db import models


class Notificacao(models.Model):
    class Canal(models.TextChoices):
        EMAIL = "EMAIL", "Email"
        PAINEL = "PAINEL", "Painel"

    titulo = models.CharField(max_length=150)
    mensagem = models.TextField()
    canal = models.CharField(max_length=10, choices=Canal.choices, default=Canal.PAINEL)
    destino = models.CharField(max_length=150, help_text="Email ou identificador do destinatário")
    disparada_em = models.DateTimeField(auto_now_add=True)
    lida = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Notificação"
        verbose_name_plural = "Notificações"

