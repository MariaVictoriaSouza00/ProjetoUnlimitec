from django.contrib import admin
from django.urls import path, include
from appUsuario.views import login_usuario
from appPesquisa.views import tela_index


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', tela_index, name='tela_index'), 
    path('usuario/', include('appUsuario.urls')),  
    path('pesquisa/', include('appPesquisa.urls')), 
]
