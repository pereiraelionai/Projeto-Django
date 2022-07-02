from django.shortcuts import redirect, render
from django.views import View
from django.http import HttpResponse
from django.views.generic.list import ListView
from .models import Servico
from . import forms
from django.contrib import messages


class CriarServico(View):
    template_name = 'servico/criar_servico.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.contexto = {
            'servicoform': forms.ServicoForm(
                data=self.request.POST or None
            )
        }

        self.servicoform = self.contexto['servicoform']

        self.renderizar = render(
            self.request, self.template_name, self.contexto
        )

    def post(self, *args, **kwargs):
        if not self.servicoform.is_valid():
            messages.error(
                self.request, 'Existem erros no formulário, por favor revise e tente novamente'
            )
            return self.renderizar

        servico_db = Servico(**self.servicoform.cleaned_data)
        servico_db.save()

        return redirect('servico:listar')

    def get(self, *args, **kwargs):
        return self.renderizar


class ListarServico(ListView):
    model = Servico
    template_name = 'servico/listar_servico.html'
    context_object_name = 'servicos'
