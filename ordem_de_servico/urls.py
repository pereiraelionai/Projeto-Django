from django.urls import path
from . import views

app_name = 'os'

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dash'),
    path('pre_os', views.PreCriarOs.as_view(), name='pre_os'),
    path('criar/', views.CriarOS.as_view(), name='criar'),
    path('add_cliente/', views.AdicionarCliente.as_view(), name='add_cliente'),
    path('add_os/', views.AdicionandoOS.as_view(), name='add_os'),
    path('add_coment/', views.AdicionandoComent.as_view(), name='add_coment'),
    path('remover_item_os/', views.RemoverItemOs.as_view(), name='remover'),
    path('listar/', views.ListarOs.as_view(), name='listar'),
    path('salvar/', views.SalvarOs.as_view(), name='salvar'),
    path('listar_os', views.ListarOrdens.as_view(), name='listar_os')
]
