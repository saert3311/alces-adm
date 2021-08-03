from django.contrib import admin
from django.urls import path
from django.conf.urls import handler404, handler500
from django.contrib.auth import views as auth_views

from . import views
from .views import *

app_name = 'app'
handler404 = views.handler404
handler500 = views.handler500

urlpatterns = [
    # Pagina Inicio
    path('', Inicio.as_view(), name='inicio'),
    path('tools/get_comunas/', views.GetComunas, name='get_comunas')
]