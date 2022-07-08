from ast import Return
import email
from pydoc import cli
from select import select
from time import timezone
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
from .models import ItemPeca, ItemServico


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
        id_cliente = info_cliente.pk

        self.request.session['cliente'] = {}
        self.request.session['cliente'] = {
            'id_cliente': id_cliente,
            'nome_cliente': nome_cliente,
            'last_cliente': sobrenome_cliente,
            'cpf_cliente': cpf_cliente,
            'telefone_cliente': telefone_cliente,
            'email_cliente': email_cliente
        }

        self.request.session.save()

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
                        f' no produto {nome_produto}. Adicionamos {estoque_produto} x'
                        f' na ordem de serviço.'
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

        return redirect(http_referer)


class AdicionandoComent(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('os:criar')
        )

        produto = self.request.session['carrinho_produto'] or None
        servico = self.request.session['carrinho_servico'] or None

        if produto == None and servico == None:
            messages.info(
                self.request, 'Crie sua ordem de serviço'
            )
            return redirect(http_referer)

        comentarios = self.request.GET.get('comentarios')
        veiculo = self.request.GET.get('veiculo')
        placa = self.request.GET.get('placa')
        km = self.request.GET.get('km')
        data = self.request.GET.get('data')
        # TODO: arrumar formato da data
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

        total_produto = float()
        total_servico = float()

        for chave_1, valor_1 in self.request.session['carrinho_produto'].items():
            for chave_2, valor_2 in valor_1.items():
                if chave_2 == 'preco_produto_os':
                    valor_2 = float(valor_2)
                    total_produto += valor_2

        for chave_1, valor_1 in self.request.session['carrinho_servico'].items():
            for chave_2, valor_2 in valor_1.items():
                if chave_2 == 'preco_servico_os':
                    valor_2 = float(valor_2)
                    total_servico += valor_2

        total_os = total_produto + total_servico
        self.request.session['total'] = {
            'valor_total': total_os
        }

        contexto = {
            'carrinho_comentario': self.request.session.get('carrinho_comentario', {}),
            'carrinho_produto': self.request.session.get('carrinho_produto', {}),
            'carrinho_servico': self.request.session.get('carrinho_servico', {}),
            'cliente': self.request.session.get('cliente', {}),
            'total_os': self.request.session.get('total', {})
        }
        return render(self.request, 'ordem_de_servico/resumo_os.html', contexto)


class SalvarOs(View):
    template_name = 'ordem_de_servico/dashboard.html'

    def get(self, *args, **kwargs):

        if not self.request.session.get('cliente'):
            messages.error(self.request, 'Selecione o cliente.')
            return redirect('os:pre_os')

        if not self.request.session.get('carrinho_produto') and not self.request.session.get('carrinho_servico'):
            messages.error(self.request, 'Selecione o produto ou serviço')
            return redirect('os:pre_os')

        carrinho_produto = self.request.session['carrinho_produto']
        carrinho_servico = self.request.session['carrinho_servico']
        carrinho_comentario = self.request.session['carrinho_comentario']
        cliente = self.request.session['cliente']['id_cliente']
        valor_total = self.request.session['total']['valor_total']

        carrinho_produto_itens = [v for v in carrinho_produto]
        carrinho_servico_itens = [v for v in carrinho_servico]
        comentario_veiculo = carrinho_comentario['veiculo']
        comentario_placa = carrinho_comentario['placa']
        comentario_km = carrinho_comentario['km']
        comentario_data_entrada = carrinho_comentario['entrada']
        comentario_data_saida = carrinho_comentario['data']
        comentario_comentario = carrinho_comentario['comentarios']

        bd_produto = list(Produto.objects.filter(id__in=carrinho_produto))
        for valor in bd_produto:
            vid = str(valor.id)

            estoque = valor.estoque
            qtd_carrinho = carrinho_produto[vid]['quantidade']
            preco_unit = carrinho_produto[vid]['preco_produto']

        cliente_db = Cliente.objects.get(pk=cliente)

        if not self.request.session.get('carrinho_servico'):
            fechar_os = True

        os = OrdemServico(
            cliente=cliente_db,
            veiculo=comentario_veiculo or 'N.A',
            placa_veiculo=comentario_placa or 'N.A',
            km=comentario_km or 0,
            data_inicial=comentario_data_entrada,
            data_termino=comentario_data_saida or f'{date.today().year}-{date.today().month}-{date.today().day}',
            valor_total=valor_total,
            observacoes=comentario_comentario or '',
            os_concluida=fechar_os
        )

        os.save()

        ItemPeca.objects.bulk_create(
            [
                ItemPeca(
                    ordem_servico=os,
                    produto=v['nome_produto'],
                    produto_id=v['produto_id'],
                    preco=v['preco_produto'],
                    quantidade=v['quantidade']
                ) for v in carrinho_produto.values()
            ]
        )

        ItemServico.objects.bulk_create(
            [
                ItemServico(
                    ordem_servico=os,
                    servico=v['nome_servico'],
                    servico_id=v['servico_id'],
                    preco=v['preco_servico']
                ) for v in carrinho_servico.values()
            ]
        )

        del self.request.session['carrinho_produto']
        del self.request.session['carrinho_servico']
        del self.request.session['cliente']
        del self.request.session['total']

        return redirect('os:dash')


# TODO: Tentar fazer função imprimir
class Imprimir(View):
    pass


class ListarOrdens(ListView):
    # TODO: corrigir a ordem de exibição...os mais recentes primeiro
    model = OrdemServico
    template_name = 'ordem_de_servico/listar_os.html'
    context_object_name = 'ordem_de_servico'
    paginate_by = 10
