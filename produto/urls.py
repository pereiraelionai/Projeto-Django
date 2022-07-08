from django.urls import path
from . import views

app_name = 'produto'

urlpatterns = [
    path('criar/', views.CriarProduto.as_view(), name='criar'),
    path('listar/', views.ListarProduto.as_view(), name='listar'),
    path('<int:produto_id>', views.detalhe_produto, name='detalhe_produto')
]
