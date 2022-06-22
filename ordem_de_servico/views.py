from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View


class Dashboard(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'ordem_de_servico/dashboard.html')


class CriarOS(View):
    pass


class ListarOs(View):
    pass
