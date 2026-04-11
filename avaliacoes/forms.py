from django import forms
from .models import Avaliacao


class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['nota', 'comentario']
        widgets = {
            'comentario': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Conte como foi sua experiência...',
                'style': 'resize: none;'
            }),
        }