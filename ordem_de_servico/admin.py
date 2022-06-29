from django.contrib import admin
from .models import OrdemServico, ItemPeca, ItemServico


class ItemPecaInline(admin.TabularInline):
    model = ItemPeca
    extra = 1


class ItemServicoInline(admin.TabularInline):
    model = ItemServico
    extra = 1


class OrdemServicoAdmin(admin.ModelAdmin):
    list_display = [
        'cliente', 'marca_veiculo', 'modelo_veiculo', 'placa_veiculo', 'data_inicial', 'data_termino'
    ]
    inlines = [
        ItemPecaInline, ItemServicoInline
    ]


admin.site.register(ItemPeca)
admin.site.register(ItemServico)
admin.site.register(OrdemServico, OrdemServicoAdmin)
