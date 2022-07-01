from django.forms import ModelForm
from .models import Cliente


class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        exclude = ('idade', 'data_criacao')
