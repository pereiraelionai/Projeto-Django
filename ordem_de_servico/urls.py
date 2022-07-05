from django.urls import path
from . import views

app_name = 'os'

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dash'),
    path('criar/', views.CriarOS.as_view(), name='criar'),
    path('listar/', views.ListarOs.as_view(), name='listar'),
    path('add_os/', views.AdicionandoOS.as_view(), name='add_os')
]
