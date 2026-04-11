from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import AvaliacaoForm
from .models import Avaliacao
from agendamentos.models import Agendamento


@login_required
def criar_avaliacao(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, id=agendamento_id)

    # Só o cliente do agendamento pode avaliar
    if request.user != agendamento.cliente:
        return HttpResponseForbidden("Somente o cliente pode avaliar este atendimento.")

    # Só pode avaliar se estiver concluído
    if agendamento.status != 'concluido':
        return HttpResponseForbidden("Só é possível avaliar atendimentos concluídos.")

    # Impede avaliação duplicada
    if hasattr(agendamento, 'avaliacao'):
        return HttpResponseForbidden("Este agendamento já foi avaliado.")

    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.agendamento = agendamento
            avaliacao.save()
            return redirect('dashboard')
    else:
        form = AvaliacaoForm()

    return render(request, 'avaliacoes/criar_avaliacao.html', {
        'form': form,
        'agendamento': agendamento
    })