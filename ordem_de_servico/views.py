import email
from django.contrib import messages
from servico.models import Servico
from produto.models import Produto
from cliente.models import Cliente
from .models import OrdemServico
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse
from email import message
from django.shortcuts import render, redirect, reverse, get_object_or_404
from datetime import date


class Dashboard(ListView):
    model = OrdemServico
    template_name = 'ordem_de_servico/dashboard.html'
    context_object_name = 'ordens'


class PreCriarOs(ListView):
    model = Cliente
    template_name = 'ordem_de_servico/add_cliente.html'
    context_object_name = 'clientes'
    paginate_by = 10


class AdicionarCliente(View):
    def get(self, *args, **kwargs):
        id_cliente = self.request.GET.get('id_cliente')
        info_cliente = get_object_or_404(Cliente, id=id_cliente)
        nome_cliente = info_cliente.nome
        sobrenome_cliente = info_cliente.sobrenome
        cpf_cliente = info_cliente.cpf
        telefone_cliente = info_cliente.telefone
        email_cliente = info_cliente.email

        self.request.session['cliente'] = {}
        self.request.session['cliente'] = {
            'nome_cliente': nome_cliente,
            'last_cliente': sobrenome_cliente,
            'cpf_cliente': cpf_cliente,
            'telefone_cliente': telefone_cliente,
            'email_cliente': email_cliente
        }

        self.request.session.save()

        print('AQUIIIIII')
        print(self.request.session['cliente'])

        return redirect('os:criar')


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

        if not self.request.session.get('carrinho_produto'):
            self.request.session['carrinho_produto'] = {}
            self.request.session.save()

        if not self.request.session.get('carrinho_servico'):
            self.request.session['carrinho_servico'] = {}
            self.request.session.save()

        carrinho_produto = self.request.session['carrinho_produto']
        carrinho_servico = self.request.session['carrinho_servico']

        # adicionando os produtos na ordem de serviço
        if id_produto != None:
            if id_produto in carrinho_produto:
                quantidade_produto_carrinho = carrinho_produto[id_produto]['quantidade']
                quantidade_produto_carrinho += 1

                if estoque_produto < quantidade_produto_carrinho:
                    messages.error(
                        self.request,
                        f'Estoque insuficiente para {quantidade_produto_carrinho} x'
                        f'no produto {nome_produto}. Adicionamos {estoque_produto} x'
                        f'na ordem de serviço.'
                    )
                    quantidade_produto_carrinho = estoque_produto

                carrinho_produto[id_produto]['quantidade'] = quantidade_produto_carrinho
                carrinho_produto[id_produto]['preco_produto_os'] = preco_produto * \
                    quantidade_produto_carrinho
            else:
                carrinho_produto[id_produto] = {
                    'produto_id': produto_id,
                    'nome_produto': nome_produto,
                    'preco_produto': preco_produto,
                    'descricao_produto': descricao_produto,
                    'quantidade': 1,
                    'preco_produto_os': preco_produto
                }

        # adicionando os serviços na ordem de serviço
        if id_servico != None:
            if id_servico in carrinho_servico:
                quantidade_servico_os = carrinho_servico[id_servico]['quantidade']
                quantidade_servico_os += 1

                carrinho_servico[id_servico]['quantidade'] = quantidade_servico_os
                carrinho_servico[id_servico]['preco_servico_os'] = preco_servico * \
                    quantidade_servico_os
            else:
                carrinho_servico[id_servico] = {
                    'servico_id': servico_id,
                    'nome_servico': nome_servico,
                    'preco_servico': preco_servico,
                    'descricao_servico': descricao_servico,
                    'quantidade': 1,
                    'preco_servico_os': preco_servico
                }

        self.request.session.save()

        print(carrinho_produto)
        print(carrinho_servico)

        return redirect(http_referer)


class AdicionandoComent(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('os:criar')
        )

        produto = self.request.session['carrinho_produto']
        servico = self.request.session['carrinho_servico']

        if produto == None or servico == None:
            messages.info(
                self.request, 'Crie sua ordem de serviço'
            )
            return redirect(http_referer)

        comentarios = self.request.GET.get('comentarios')
        veiculo = self.request.GET.get('veiculo')
        placa = self.request.GET.get('placa')
        km = self.request.GET.get('km')
        data = self.request.GET.get('data')
        entrada = '{}-{}-{}'.format(date.today().day,
                                    date.today().month, date.today().year)

        self.request.session['carrinho_comentario'] = {
            'veiculo': veiculo,
            'placa': placa,
            'km': km,
            'entrada': entrada,
            'data': data,
            'comentarios': comentarios
        }

        self.request.session.save()

        print(self.request.session['carrinho_comentario'])

        return redirect('os:listar')


class RemoverItemOs(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('os:pre_os')
        )

        id_produto_remove = self.request.GET.get('id_produto')
        id_servico_remove = self.request.GET.get('id_servico')

        if id_produto_remove:
            if not self.request.session['carrinho_produto']:
                return redirect(http_referer)

            if not id_produto_remove:
                return redirect(http_referer)

            if not id_produto_remove in self.request.session['carrinho_produto']:
                return redirect(http_referer)
            carrinho = self.request.session['carrinho_produto'][id_produto_remove]

            # TODO: verificar pois a mensagem aparece no local errado
            messages.success(
                self.request,
                f'Produto {carrinho["nome_produto"]} removido com sucesso'
            )

            del self.request.session['carrinho_produto'][id_produto_remove]
            self.request.session.save()
            return redirect(http_referer)

        if id_servico_remove:
            if not self.request.session['carrinho_servico']:
                return redirect(http_referer)

            if not id_servico_remove:
                return redirect(http_referer)

            if not id_servico_remove in self.request.session['carrinho_servico']:
                return redirect(http_referer)

            carrinho = self.request.session['carrinho_servico'][id_servico_remove]
            # TODO: verificar pois a mensagem aparece no local errado
            messages.success(
                self.request,
                f'Produto {carrinho["nome_servico"]} removido com sucesso'
            )

            del self.request.session['carrinho_servico'][id_servico_remove]
            self.request.session.save()
            return redirect(http_referer)

        return redirect(http_referer)


class ListarOs(View):
    def get(self, *args, **kwargs):
        contexto = {
            'carrinho_comentario': self.request.session.get('carrinho_comentario', {}),
            'carrinho_produto': self.request.session.get('carrinho_produto', {}),
            'carrinho_servico': self.request.session.get('carrinho_servico', {}),
            'cliente': self.request.session.get('cliente', {})
        }
        return render(self.request, 'ordem_de_servico/resumo_os.html', contexto)
