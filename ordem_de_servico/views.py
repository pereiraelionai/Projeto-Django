from django.contrib import messages
from servico.models import Servico
from produto.models import Produto
from .models import OrdemServico
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse
from email import message
from django.shortcuts import render, redirect, reverse, get_object_or_404


class Dashboard(ListView):
    model = OrdemServico
    template_name = 'ordem_de_servico/dashboard.html'
    context_object_name = 'ordens'


class CriarOS(ListView):
    model = Produto
    template_name = 'ordem_de_servico/criar_os_servico.html'
    context_object_name = 'os_produtos'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(CriarOS, self).get_context_data(**kwargs)
        context.update({
            'os_servicos': Servico.objects.order_by('nome_servico')
        })

        return context


class AdicionandoOS(View):
    def get(self, *args, **kwargs):

        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('os:criar')
        )

        # carregando o Id pelo GET
        id_produto = self.request.GET.get('id_produto')
        id_servico = self.request.GET.get('id_servico')
        comentarios = self.request.GET.get('comentarios')

        if not id_servico and not id_produto and not comentarios:
            messages.info(
                self.request, 'Crie sua ordem de serviço'
            )
            return redirect(http_referer)

        # buscando o produto no banco de dados
        if id_produto:
            produto = get_object_or_404(Produto, id=id_produto)
            messages.success(
                self.request,
                f'{produto.nome_produto} adicionado com sucesso'
            )

            produto_id = produto.pk
            nome_produto = produto.nome_produto
            preco_produto = produto.preco_produto
            descricao_produto = produto.descricao_produto
            estoque_produto = produto.estoque

            if estoque_produto < 1:
                messages.error(
                    self.request,
                    'Estoque insuficiente'
                )
                return redirect(http_referer)

        # buscando serviço no banco de dados
        if id_servico:
            servico = get_object_or_404(Servico, id=id_servico)
            messages.success(
                self.request,
                f'{servico.nome_servico} adicionado com sucesso'
            )

            servico_id = servico.pk
            nome_servico = servico.nome_servico
            preco_servico = servico.preco_servico
            descricao_servico = servico.descricao_servico

        if not self.request.session.get('carrinho_os'):
            self.request.session['carrinho_os'] = {}
            self.request.session['carrinho_os']['id_produto'] = {}
            self.request.session['carrinho_os']['id_servico'] = {}
            self.request.session.save()

        carrinho_os = self.request.session['carrinho_os']

        # adicionando os produtos na ordem de serviço
        if id_produto in carrinho_os['id_produto']:
            quantidade_produto_carrinho = carrinho_os['id_produto'][id_produto]['quantidade']
            quantidade_produto_carrinho += 1

            if estoque_produto < quantidade_produto_carrinho:
                messages.error(
                    self.request,
                    f'Estoque insuficiente para {quantidade_produto_carrinho} x'
                    f'no produto {nome_produto}. Adicionamos {estoque_produto} x'
                    f'na ordem de serviço.'
                )
                quantidade_produto_carrinho = estoque_produto

            carrinho_os['id_produto'][id_produto]['quantidade'] = quantidade_produto_carrinho
            carrinho_os['id_produto'][id_produto]['preco_produto_os'] = preco_produto * \
                quantidade_produto_carrinho
        else:
            carrinho_os['id_produto'][id_produto] = {
                'produto_id': produto_id,
                'nome_produto': nome_produto,
                'preco_produto': preco_produto,
                'descricao_produto': descricao_produto,
                'quantidade': 1,
                'preco_produto_os': preco_produto
            }

        # adicionando os serviços na ordem de serviço
        if id_servico in carrinho_os['id_servico']:
            quantidade_servico_os = carrinho_os['id_servico'][id_servico]['quantidade']
            quantidade_servico_os += 1

            carrinho_os['id_servico'][id_servico]['quantidade'] = quantidade_servico_os
            carrinho_os['id_servico'][id_servico]['preco_servico_os'] = preco_servico * \
                quantidade_servico_os
        else:
            carrinho_os['id_servico'][id_servico] = {
                'servico_id': servico_id,
                'nome_servico': nome_servico,
                'preco_servico': preco_servico,
                'descricao_servico': descricao_servico,
                'quantidade': 1,
                'preco_servico_os': preco_servico
            }

        carrinho_os['comentarios'] = {
            'comentarios': comentarios
        }

        self.request.session.save()

        return redirect(http_referer)


class ListarOs(View):
    pass
