from django.db import models
from django.utils import timezone


class OrdemServico(models.Model):
    cliente = models.CharField(max_length=50)
    marca_veiculo = models.CharField(max_length=50)
    modelo_veiculo = models.CharField(max_length=100)
    placa_veiculo = models.CharField(max_length=8)
    km = models.PositiveIntegerField()
    data_inicial = models.DateField(auto_now=True, verbose_name='Data')
    data_termino = models.DateTimeField(
        default=timezone.now, verbose_name='Data Término')
    observacoes = models.TextField()

    def __str__(self):
        return f'OS Nº {self.pk}'


class ItemPeca(models.Model):
    ordem_servico = models.ForeignKey(OrdemServico, on_delete=models.CASCADE)
    produto = models.CharField(max_length=100)
    produto_id = models.PositiveIntegerField()
    preco = models.FloatField()
    quantidade = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.ordem_servico}'


class ItemServico(models.Model):
    ordem_servico = models.ForeignKey(OrdemServico, on_delete=models.CASCADE)
    servico = models.CharField(max_length=100)
    servico_id = models.PositiveIntegerField()
    preco = models.FloatField()

    def __str__(self):
        return f'{self.ordem_servico}'
