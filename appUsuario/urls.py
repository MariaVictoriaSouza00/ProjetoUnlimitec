from django.urls import path
from .views import cadastro_usuario
from .views import login_usuario
from .views import carregar_cidades



urlpatterns = [
    path('cadastro/', cadastro_usuario, name='cadastro_usuario'),
    path('login/', login_usuario, name='login_usuario'),
      path('ajax/carregar-cidades/', carregar_cidades, name='carregar_cidades'),
]
