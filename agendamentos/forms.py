from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Agendamento


class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['servico', 'prestador', 'data', 'horario', 'observacao']
        widgets = {
            'data': forms.DateInput(attrs={
                'type': 'date',
                'min': timezone.localdate().isoformat()
            }),
            'horario': forms.TimeInput(attrs={'type': 'time'}),
            'observacao': forms.Textarea(attrs={
                'rows': 4,
                'style': 'resize: none;'
            }),
        }

    def __init__(self, *args, **kwargs):
        self.usuario_logado = kwargs.pop('usuario_logado', None)
        super().__init__(*args, **kwargs)

        # Na carga inicial, mostra todos os prestadores
        self.fields['prestador'].queryset = User.objects.filter(
            perfil__tipo_usuario='prestador'
        ).distinct()

        servico_id = None

        # Quando o formulário já vem preenchido/enviado
        if self.is_bound:
            try:
                servico_id = int(self.data.get('servico'))
            except (TypeError, ValueError):
                servico_id = None

        # Quando estiver editando uma instância já existente
        elif self.instance.pk and self.instance.servico_id:
            servico_id = self.instance.servico_id

        # Se um serviço foi escolhido, filtra só os prestadores desse serviço
        if servico_id:
            self.fields['prestador'].queryset = User.objects.filter(
                perfil__tipo_usuario='prestador',
                perfil__servicos_oferecidos__id=servico_id
            ).distinct()

    def clean(self):
        cleaned_data = super().clean()
        prestador = cleaned_data.get('prestador')
        servico = cleaned_data.get('servico')
        data = cleaned_data.get('data')
        horario = cleaned_data.get('horario')

        hoje = timezone.localdate()

        # Impede data passada
        if data and data < hoje:
            raise forms.ValidationError(
                'Não é permitido criar agendamento em data passada.'
            )

        # Impede auto seleção
        if prestador and self.usuario_logado and prestador == self.usuario_logado:
            raise forms.ValidationError(
                'Você não pode selecionar a si mesmo como prestador.'
            )

        # Garante que o usuário escolhido tem perfil
        if prestador and not hasattr(prestador, 'perfil'):
            raise forms.ValidationError(
                'O usuário selecionado não possui perfil válido.'
            )

        # Garante que o prestador oferece o serviço escolhido
        if prestador and servico:
            if not prestador.perfil.servicos_oferecidos.filter(id=servico.id).exists():
                raise forms.ValidationError(
                    'O prestador selecionado não oferece este serviço.'
                )

        # Impede conflito de horário para o mesmo prestador
        if prestador and data and horario:
            conflito = Agendamento.objects.filter(
                prestador=prestador,
                data=data,
                horario=horario
            ).exclude(status='cancelado')

            if self.instance.pk:
                conflito = conflito.exclude(pk=self.instance.pk)

            if conflito.exists():
                raise forms.ValidationError(
                    'Este prestador já possui um agendamento neste mesmo dia e horário.'
                )

        return cleaned_data


class StatusAgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['status']

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)

        self.fields['status'].choices = []

        if not usuario or not self.instance:
            return

        status_atual = self.instance.status

        # Não altera finalizados
        if status_atual in ['cancelado', 'concluido']:
            self.fields['status'].choices = []
            return

        if hasattr(usuario, 'perfil'):
            tipo = usuario.perfil.tipo_usuario

            # Cliente só pode cancelar
            if tipo == 'cliente' and status_atual in ['pendente', 'confirmado']:
                self.fields['status'].choices = [
                    ('cancelado', 'Cancelado'),
                ]

            # Prestador confirma pendente
            elif tipo == 'prestador' and status_atual == 'pendente':
                self.fields['status'].choices = [
                    ('confirmado', 'Confirmado'),
                ]

            # Prestador conclui confirmado
            elif tipo == 'prestador' and status_atual == 'confirmado':
                self.fields['status'].choices = [
                    ('concluido', 'Concluído'),
                ]