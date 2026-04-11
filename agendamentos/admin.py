from django.contrib import admin
from .models import Agendamento

@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'prestador', 'servico', 'data', 'horario', 'status')
    list_filter = ('status', 'data')
    search_fields = ('cliente__username', 'prestador__username', 'servico__nome')