from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from agendamentos.models import Agendamento

class Avaliacao(models.Model):
    agendamento = models.OneToOneField(Agendamento, on_delete=models.CASCADE)
    nota = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comentario = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Avaliação - {self.agendamento.cliente.username} - Nota {self.nota}'