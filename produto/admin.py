from django.contrib import admin
from .models import Produto


class ProdutoAdmin(admin.ModelAdmin):
    list_display = [
        'nome_produto', 'descricao_produto', 'estoque', 'preco_produto'
    ]


admin.site.register(Produto, ProdutoAdmin)
