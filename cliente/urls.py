from django.urls import path
from . import views

app_name = 'cliente'

urlpatterns = [
    path('criar/', views.CriarCliente.as_view(), name='criar'),
    path('listar/', views.ListarCliente.as_view(), name='listar'),
    path('<int:cliente_id>', views.ver_cliente, name='ver_cliente')
]
