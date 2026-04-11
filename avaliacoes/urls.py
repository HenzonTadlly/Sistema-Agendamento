from django.urls import path
from .views import criar_avaliacao

urlpatterns = [
    path('agendamento/<int:agendamento_id>/nova/', criar_avaliacao, name='criar_avaliacao'),
]