from django.urls import path
from .views import home, cadastro, login_view, dashboard, logout_view, editar_perfil

urlpatterns = [
    path('', home, name='home'),
    path('cadastro/', cadastro, name='cadastro'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('perfil/', editar_perfil, name='editar_perfil'),
]