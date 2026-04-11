from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Perfil


class CadastroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)

    TIPO_USUARIO_CHOICES = (
        ('cliente', 'Cliente'),
        ('prestador', 'Prestador'),
    )

    tipo_usuario = forms.ChoiceField(choices=TIPO_USUARIO_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'tipo_usuario']


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['foto', 'telefone', 'descricao', 'servicos_oferecidos']
        widgets = {
            'foto': forms.FileInput(attrs={'accept': 'image/*', 'id': 'id_foto'}),
            'telefone': forms.TextInput(attrs={'placeholder': 'Digite seu telefone'}),
            'descricao': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': 'Escreva uma breve descrição sobre você...',
                'style': 'resize: none;'
            }),
            'servicos_oferecidos': forms.CheckboxSelectMultiple(),
        }