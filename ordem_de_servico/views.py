from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.views.generic.list import ListView
from .models import OrdemServico


class Dashboard(ListView):
    model = OrdemServico
    template_name = 'ordem_de_servico/dashboard.html'
    context_object_name = 'ordens'


class CriarOS(View):
    pass


class ListarOs(View):
    pass
