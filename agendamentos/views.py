from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import AgendamentoForm, StatusAgendamentoForm
from .models import Agendamento


@login_required
def criar_agendamento(request):
    if hasattr(request.user, 'perfil') and request.user.perfil.tipo_usuario != 'cliente':
        messages.error(request, 'Apenas clientes podem criar agendamentos.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = AgendamentoForm(request.POST, usuario_logado=request.user)
        if form.is_valid():
            agendamento = form.save(commit=False)
            agendamento.cliente = request.user
            agendamento.save()
            messages.success(request, 'Agendamento criado com sucesso.')
            return redirect('dashboard')
        messages.error(request, 'Não foi possível criar o agendamento. Verifique os dados informados.')
    else:
        form = AgendamentoForm(usuario_logado=request.user)

    return render(request, 'agendamentos/criar_agendamento.html', {'form': form})


@login_required
def alterar_status_agendamento(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, id=agendamento_id)

    if request.user != agendamento.cliente and request.user != agendamento.prestador:
        messages.error(request, 'Você não tem permissão para alterar este agendamento.')
        return redirect('dashboard')

    status_atual = agendamento.status

    if status_atual in ['cancelado', 'concluido']:
        messages.warning(request, 'Este agendamento não pode mais ser alterado.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = StatusAgendamentoForm(
            request.POST,
            instance=agendamento,
            usuario=request.user
        )

        if form.is_valid():
            novo_status = form.cleaned_data['status']

            if request.user == agendamento.cliente:
                if novo_status != 'cancelado':
                    messages.error(request, 'Cliente só pode cancelar o agendamento.')
                    return redirect('dashboard')

                if status_atual not in ['pendente', 'confirmado']:
                    messages.error(request, 'Este agendamento não pode ser cancelado pelo cliente.')
                    return redirect('dashboard')

            elif request.user == agendamento.prestador:
                if novo_status == 'confirmado':
                    if status_atual != 'pendente':
                        messages.error(request, 'Só é possível confirmar agendamento pendente.')
                        return redirect('dashboard')

                elif novo_status == 'concluido':
                    if status_atual != 'confirmado':
                        messages.error(request, 'Só é possível concluir agendamento confirmado.')
                        return redirect('dashboard')

                else:
                    messages.error(request, 'Prestador só pode confirmar ou concluir o agendamento.')
                    return redirect('dashboard')

            agendamento.status = novo_status
            agendamento.save()
            messages.success(request, 'Status atualizado com sucesso.')
            return redirect('dashboard')

        messages.error(request, 'Não foi possível atualizar o status.')
        return redirect('dashboard')

    form = StatusAgendamentoForm(instance=agendamento, usuario=request.user)

    return render(request, 'agendamentos/alterar_status.html', {
        'form': form,
        'agendamento': agendamento
    })


@login_required
def atualizar_status_rapido(request, agendamento_id, novo_status):
    agendamento = get_object_or_404(Agendamento, id=agendamento_id)

    if request.method != 'POST':
        messages.error(request, 'Método inválido para esta ação.')
        return redirect('dashboard')

    if request.user != agendamento.cliente and request.user != agendamento.prestador:
        messages.error(request, 'Você não tem permissão para alterar este agendamento.')
        return redirect('dashboard')

    status_atual = agendamento.status

    if status_atual in ['cancelado', 'concluido']:
        messages.warning(request, 'Este agendamento não pode mais ser alterado.')
        return redirect('dashboard')

    if request.user == agendamento.cliente:
        if novo_status != 'cancelado':
            messages.error(request, 'Cliente só pode cancelar o agendamento.')
            return redirect('dashboard')

        if status_atual not in ['pendente', 'confirmado']:
            messages.error(request, 'Este agendamento não pode ser cancelado.')
            return redirect('dashboard')

    elif request.user == agendamento.prestador:
        if novo_status == 'confirmado':
            if status_atual != 'pendente':
                messages.error(request, 'Só é possível confirmar agendamento pendente.')
                return redirect('dashboard')

        elif novo_status == 'concluido':
            if status_atual != 'confirmado':
                messages.error(request, 'Só é possível concluir agendamento confirmado.')
                return redirect('dashboard')

        else:
            messages.error(request, 'Prestador só pode confirmar ou concluir o agendamento.')
            return redirect('dashboard')

    agendamento.status = novo_status
    agendamento.save()
    messages.success(request, 'Status atualizado com sucesso.')
    return redirect('dashboard')