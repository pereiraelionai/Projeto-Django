from pyexpat import model
from django.db import models
from django.utils.text import slugify


class Produto(models.Model):
    nome_produto = models.CharField(max_length=50)
    preco_produto = models.FloatField()
    descricao_produto = models.CharField(max_length=250)
    decricao_detalhada_produto = models.TextField()
    # TODO: Inserir imagem genérica caso não seja inserida a imagem
    imagem_produto = models.ImageField(
        upload_to='produto_images/%Y/%m', blank=True, null=True
    )
    estoque = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.nome_produto)}'
            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.nome_produto}'
