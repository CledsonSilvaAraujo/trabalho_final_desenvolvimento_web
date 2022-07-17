from django.urls import path
from produto import views

app_name = 'produto'

urlpatterns = [
    path('', views.index, name='index'),
    path('cadastra_produto/', views.cadastra_produto, name='cadastra_produto'),
    path('lista_produto/', views.lista_produto, name='lista_produto'),
    path('edita_produto/', views.edita_produto, name='edita_produto'),
    path('deleta_produto/', views.deleta_produto, name='deleta_produto'),
   
]