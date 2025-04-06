from django.contrib import admin
from django.urls import path, include
from appUsuario.views import login_usuario


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_usuario, name='login_usuario'), 
    path('usuario/', include('appUsuario.urls')),   
]
