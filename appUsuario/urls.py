from django.urls import path
from .views import cadastro_usuario
from .views import login_usuario


urlpatterns = [
    path('cadastro/', cadastro_usuario, name='cadastro_usuario'),
    path('login/', login_usuario, name='login_usuario'),
]
