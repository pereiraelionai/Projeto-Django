from dataclasses import fields
import imp
from django.forms import ModelForm
from .models import Produto


class ProdutoForm(ModelForm):
    class Meta:
        model = Produto
        fields = '__all__'
        exclude = ('slug', )
