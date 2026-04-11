from django.contrib import admin
from .models import Avaliacao

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('agendamento', 'nota', 'criado_em')
    list_filter = ('nota', 'criado_em')
    search_fields = ('agendamento__cliente__username', 'agendamento__prestador__username')