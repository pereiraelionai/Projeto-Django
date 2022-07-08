import imp
from this import s
from urllib import request
from django.shortcuts import get_list_or_404, redirect, render
from django.views import View
from django.views.generic.list import ListView
from django.http import HttpResponse

from ordem_de_servico import views
from .models import Produto
from . import forms
from django.contrib import messages


class CriarProduto(View):
    template_name = 'produto/criar_produto.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.contexto = {
            'produtoform': forms.ProdutoForm(
                data=self.request.POST or None
            )
        }

        self.produtoform = self.contexto['produtoform']

        self.renderizar = render(
            self.request, self.template_name, self.contexto
        )

    def post(self, *args, **kwargs):
        if not self.produtoform.is_valid():
            messages.error(
                self.request, 'Existem erros no formulário, por favor revise e tente novamente'
            )
            return self.renderizar
        '''
        produto_db = Produto(**self.produtoform.cleaned_data)
        # TODO: Inserir mensagens de sucesso ao salvar o produto
        produto_db.save()
        '''
        if self.request.method == 'POST':
            form = forms.ProdutoForm(self.request.POST, self.request.FILES)
            if form.is_valid():
                form.save()
                return redirect('produto:listar')
            else:
                form = forms.ProdutoForm()

        return self.renderizar

    def get(self, *args, **kwars):
        return self.renderizar


class ListarProduto(ListView):
    model = Produto
    template_name = 'produto/listar_produtos.html'
    context_object_name = 'produtos'
    paginate_by = 10


def detalhe_produto(request, produto_id):
    produto = get_list_or_404(Produto.objects.values(), id=produto_id)

    return render(request, 'produto/detalhe_produto.html', {
        'produtos': produto
    })
