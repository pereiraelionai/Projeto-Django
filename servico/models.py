from django.db import models


class Servico(models.Model):
    nome_servico = models.CharField(max_length=30)
    preco_servico = models.FloatField()
    descricao_servico = models.TextField()

    def __str__(self):
        return f'{self.nome_servico}'
