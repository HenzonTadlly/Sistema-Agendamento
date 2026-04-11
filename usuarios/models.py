from django.db import models
from django.contrib.auth.models import User
from servicos.models import Servico


class Perfil(models.Model):
    TIPO_USUARIO_CHOICES = (
        ('cliente', 'Cliente'),
        ('prestador', 'Prestador'),
    )

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil'
    )
    tipo_usuario = models.CharField(
        max_length=20,
        choices=TIPO_USUARIO_CHOICES,
        default='cliente'
    )
    foto = models.ImageField(
        upload_to='perfil_fotos/',
        blank=True,
        null=True
    )
    telefone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )
    descricao = models.TextField(
        blank=True,
        null=True
    )

    servicos_oferecidos = models.ManyToManyField(
        Servico,
        blank=True,
        related_name='prestadores'
    )

    def __str__(self):
        return f'{self.usuario.username} - {self.tipo_usuario}'