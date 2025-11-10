from django.db import models


class Empresa(models.Model):
    razao_social = models.CharField("Razão Social", max_length=200)
    nome_fantasia = models.CharField("Nome Fantasia", max_length=200, blank=True, null=True)
    cnpj = models.CharField("CNPJ", max_length=18, unique=True)
    telefone = models.CharField("Telefone", max_length=30, blank=True, null=True)
    endereco = models.CharField("Endereço", max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.razao_social} ({self.cnpj})"

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"


class Unidade(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="unidades")
    nome = models.CharField("Nome da Unidade", max_length=150)
    cnpj = models.CharField("CNPJ", max_length=18, blank=True, null=True)
    endereco = models.CharField("Endereço", max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Unidade"
        verbose_name_plural = "Unidades"
        unique_together = ("empresa", "nome")

    def __str__(self) -> str:
        return f"{self.nome} - {self.empresa.nome_fantasia or self.empresa.razao_social}"


class Setor(models.Model):
    unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE, related_name="setores")
    nome = models.CharField("Nome do Setor", max_length=150)

    class Meta:
        verbose_name = "Setor"
        verbose_name_plural = "Setores"
        unique_together = ("unidade", "nome")

    def __str__(self) -> str:
        return f"{self.nome} - {self.unidade}"


class Funcao(models.Model):
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE, related_name="funcoes")
    nome = models.CharField("Nome da Função", max_length=150)
    descricao = models.TextField("Descrição das Atividades", blank=True, null=True)

    class Meta:
        verbose_name = "Função"
        verbose_name_plural = "Funções"
        unique_together = ("setor", "nome")

    def __str__(self) -> str:
        return f"{self.nome} - {self.setor}"


class AmbienteTrabalho(models.Model):
    unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE, related_name="ambientes")
    nome = models.CharField("Nome do Ambiente", max_length=150)
    descricao = models.TextField("Descrição", blank=True, null=True)

    class Meta:
        verbose_name = "Ambiente de Trabalho"
        verbose_name_plural = "Ambientes de Trabalho"
        unique_together = ("unidade", "nome")

    def __str__(self) -> str:
        return f"{self.nome} - {self.unidade}"

