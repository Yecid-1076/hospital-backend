from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registro/paciente/', views.registro_paciente, name='registro-paciente'),
    path('perfil/', views.perfil_usuario, name='perfil-usuario'),
    path('logout/', views.logout, name='logout'),
]