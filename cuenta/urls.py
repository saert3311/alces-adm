from django.urls import path
from django.contrib.auth import views as auth_views
from .views import Login, ListarUsuarios, EliminarUsuario, CrearUsuario, ActualizarUsuario

app_name = "cuenta"

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='cuenta/logout.html'), name='logout'),
    path('usuarios/', ListarUsuarios.as_view(), name='usuarios'),
    path('usuarios/crear/', CrearUsuario.as_view(), name='crear_usuario'),
    path('usuarios/actualizar/<int:pk>/', ActualizarUsuario.as_view(), name='actualizar_usuario'),
    path('usuarios/eliminar/<int:pk>/', EliminarUsuario.as_view(), name='eliminar_usuario')
]
