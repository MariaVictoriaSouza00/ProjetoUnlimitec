from django.urls import path
from . import views 
from .views import tela_index, buscar_titulos_ajax

urlpatterns = [
    path('index/', tela_index, name='tela_index'),
    path('healthz', views.health_check, name='health_check'),
    path('buscar-titulos/', buscar_titulos_ajax, name='buscar_titulos_ajax'),
     path('fomento/', views.fomento, name='fomento'),
    path('definicao/', views.definicao, name='definicao'),
]
