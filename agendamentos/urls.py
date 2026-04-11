from django.urls import path
from .views import criar_agendamento, alterar_status_agendamento, atualizar_status_rapido

urlpatterns = [
    path('novo/', criar_agendamento, name='criar_agendamento'),
    path('<int:agendamento_id>/status/', alterar_status_agendamento, name='alterar_status_agendamento'),
    path('<int:agendamento_id>/status/<str:novo_status>/', atualizar_status_rapido, name='atualizar_status_rapido'),
]