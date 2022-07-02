from dataclasses import fields
from django.forms import ModelForm
from .models import Servico


class ServicoForm(ModelForm):
    class Meta:
        model = Servico
        fields = '__all__'
