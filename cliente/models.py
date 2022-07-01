from email.policy import default
from django.db import models
from django.forms import DateTimeField
from django.utils import timezone
from funcoes.validacpf import valida_cpf


class Cliente(models.Model):
    nome = models.CharField(max_length=30)
    sobrenome = models.CharField(max_length=50, default="")
    idade = models.PositiveIntegerField()
    data_nascimento = models.DateField()
    # TODO: Colocar CPF único que não funciona
    cpf = models.CharField(max_length=11, default="")
    telefone = models.CharField(max_length=16, default='')
    email = models.EmailField(default='')
    endereco = models.CharField(max_length=150)
    numero = models.CharField(max_length=5)
    bairro = models.CharField(max_length=30)
    complemento = models.CharField(max_length=30, blank=True, null=True)
    cep = models.CharField(max_length=8)
    cidade = models.CharField(max_length=30)
    data_criacao = models.DateTimeField(default=timezone.now)
    estado = models.CharField(
        default='SP',
        max_length=2,
        choices=(
            ('AC', 'Acre'),
            ('AL', 'Alagoas'),
            ('AP', 'Amapá'),
            ('AM', 'Amazonas'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'),
            ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'),
            ('PA', 'Pará'),
            ('PB', 'Paraíba'),
            ('PR', 'Paraná'),
            ('PE', 'Pernambuco'),
            ('PI', 'Piauí'),
            ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'),
            ('SE', 'Sergipe'),
            ('TO', 'Tocantins')
        )
    )

    # TODO: Finalizar validação de CPF
    '''
    def clean(self):
        erro_mesages = {}

        cpf_enviado = self.cpf or None
        cpf_salvo = None

        cliente = Cliente.objects.filter(cpf=cpf_enviado).first()
    '''
    # aparecer o nome no admin

    def __str__(self):
        return f'{self.nome} {self.sobrenome}'
