import imp
from tkinter import N
from django.shortcuts import redirect, render, get_list_or_404
from django.views import View
from django.views.generic.list import ListView
from . import forms
from django.contrib import messages
from datetime import date, datetime

import cliente
from .models import Cliente
from django.http import HttpResponse


class CriarCliente(View):
    template_name = 'cliente/criar.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.cliente = None
        id_cliente_atualizar = self.request.GET.get('id_cliente_atualizar')

        if id_cliente_atualizar:
            self.cliente = Cliente.objects.filter(
                id=id_cliente_atualizar).first()
            self.contexto = {
                'clienteform': forms.ClienteForm(
                    data=self.request.POST or None,
                    instance=self.cliente
                )
            }
        else:

            self.contexto = {
                'clienteform': forms.ClienteForm(
                    data=self.request.POST or None
                )
            }

        self.clienteform = self.contexto['clienteform']

        self.renderizar = render(
            self.request, self.template_name, self.contexto)

    def post(self, *args, **kwargs):
        if not self.clienteform.is_valid():
            messages.error(
                self.request, 'Existem erros no formulário, por favor revise e tente novamente'
            )
            return self.renderizar

        # TODO: Criar função e inserir no utils que calcule a idade co precisão
        data_nascimento = self.clienteform.cleaned_data.get('data_nascimento')
        data_atual = date.today().year
        idade = data_atual - data_nascimento.year

        self.clienteform.cleaned_data['idade'] = idade
        idade_db = Cliente(**self.clienteform.cleaned_data)
        idade_db.save()

        return redirect('cliente:listar')

    def get(self, *args, **kwargs):
        return self.renderizar


class ListarCliente(ListView):
    model = Cliente
    template_name = 'cliente/listar.html'
    context_object_name = 'clientes'
    paginate_by = 10


def ver_cliente(request, cliente_id):
    cliente = get_list_or_404(Cliente.objects.values(), id=cliente_id)

    return render(request, 'cliente/ver_cliente.html', {
        'clientes': cliente
    })


class Atualizar(CriarCliente):
    template_name = 'cliente/atualizar_cliente.html'

    def post(self, *args, **kwargs):

        atualizar_cliente = self.clienteform.save(commit=False)
        atualizar_cliente.save()

        return redirect('cliente:listar')
