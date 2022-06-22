from django.urls import path
from . import views

app_name = 'servico'

urlpatterns = [
    path('criar/', views.CriarServico.as_view(), name='criar'),
    path('listar/', views.ListarServico.as_view(), name='listar')
]
