from django.db import models
from django.contrib.auth.models import User
from servicos.models import Servico


class Agendamento(models.Model):
    STATUS_CHOICES = (
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    )

    cliente = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='agendamentos_como_cliente'
    )

    prestador = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='agendamentos_como_prestador'
    )

    servico = models.ForeignKey(
        Servico,
        on_delete=models.CASCADE
    )

    data = models.DateField()
    horario = models.TimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendente'
    )

    observacao = models.TextField(blank=True, null=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.cliente.username} - {self.servico.nome} - {self.data} {self.horario}'

    def save(self, *args, **kwargs):
        # Se já existe (edição)
        if self.pk:
            antigo = Agendamento.objects.get(pk=self.pk)

            # Bloqueia alterações em cancelado
            if antigo.status == 'cancelado':
                raise ValueError("Não é possível alterar um agendamento cancelado.")

            # Bloqueia alterações em concluído
            if antigo.status == 'concluido':
                raise ValueError("Não é possível alterar um agendamento concluído.")

        super().save(*args, **kwargs)