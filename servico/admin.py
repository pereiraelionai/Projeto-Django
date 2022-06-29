from django.contrib import admin
from .models import Servico


class ServicoAdmin(admin.ModelAdmin):
    list_display = [
        'nome_servico', 'preco_servico', 'descricao_servico'
    ]


admin.site.register(Servico, ServicoAdmin)
