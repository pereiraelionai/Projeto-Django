from django.urls import path
from . import views

app_name = 'servico'

urlpatterns = [
    path('criar/', views.CriarServico.as_view(), name='criar'),
    path('listar/', views.ListarServico.as_view(), name='listar'),
    path('<int:id_servico>', views.detalhe_servico, name='detalhe_servico'),
    path('atualizar/', views.Atualizar.as_view(), name='atualizar_servico')
]
