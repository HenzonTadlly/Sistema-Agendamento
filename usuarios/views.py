from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Avg

from .forms import CadastroUsuarioForm, PerfilForm
from agendamentos.models import Agendamento
from avaliacoes.models import Avaliacao


def home(request):
    return render(request, 'home.html')


def cadastro(request):
    if request.method == 'POST':
        form = CadastroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()

            tipo = form.cleaned_data.get('tipo_usuario')
            usuario.perfil.tipo_usuario = tipo
            usuario.perfil.save()

            login(request, usuario)
            return redirect('home')
    else:
        form = CadastroUsuarioForm()

    return render(request, 'cadastro.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            return redirect('/dashboard/')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def dashboard(request):
    tipo_usuario = request.user.perfil.tipo_usuario

    context = {
        'tipo_usuario': tipo_usuario,
    }

    if tipo_usuario == 'cliente':
        agendamentos_cliente = Agendamento.objects.filter(
            cliente=request.user
        ).order_by('-data', '-horario')

        total_cliente = agendamentos_cliente.count()
        pendentes_cliente = agendamentos_cliente.filter(status='pendente').count()
        confirmados_cliente = agendamentos_cliente.filter(status='confirmado').count()
        concluidos_cliente = agendamentos_cliente.filter(status='concluido').count()
        cancelados_cliente = agendamentos_cliente.filter(status='cancelado').count()

        agendamentos_avaliados_ids = [
            agendamento.id
            for agendamento in agendamentos_cliente
            if hasattr(agendamento, 'avaliacao')
        ]

        context.update({
            'agendamentos_cliente': agendamentos_cliente,
            'total_cliente': total_cliente,
            'pendentes_cliente': pendentes_cliente,
            'confirmados_cliente': confirmados_cliente,
            'concluidos_cliente': concluidos_cliente,
            'cancelados_cliente': cancelados_cliente,
            'grafico_cliente': [
                pendentes_cliente,
                confirmados_cliente,
                concluidos_cliente,
                cancelados_cliente,
            ],
            'agendamentos_avaliados_ids': agendamentos_avaliados_ids,
        })

    elif tipo_usuario == 'prestador':
        agendamentos_prestador = Agendamento.objects.filter(
            prestador=request.user
        ).order_by('-data', '-horario')

        total_prestador = agendamentos_prestador.count()
        pendentes_prestador = agendamentos_prestador.filter(status='pendente').count()
        confirmados_prestador = agendamentos_prestador.filter(status='confirmado').count()
        concluidos_prestador = agendamentos_prestador.filter(status='concluido').count()
        cancelados_prestador = agendamentos_prestador.filter(status='cancelado').count()

        avaliacoes_prestador = agendamentos_prestador.filter(avaliacao__isnull=False)
        total_avaliacoes_prestador = avaliacoes_prestador.count()
        media_avaliacoes_prestador = avaliacoes_prestador.aggregate(
            media=Avg('avaliacao__nota')
        )['media']

        ultimas_avaliacoes = Avaliacao.objects.filter(
            agendamento__prestador=request.user
        ).order_by('-criado_em')[:5]

        context.update({
            'agendamentos_prestador': agendamentos_prestador,
            'total_prestador': total_prestador,
            'pendentes_prestador': pendentes_prestador,
            'confirmados_prestador': confirmados_prestador,
            'concluidos_prestador': concluidos_prestador,
            'cancelados_prestador': cancelados_prestador,
            'total_avaliacoes_prestador': total_avaliacoes_prestador,
            'media_avaliacoes_prestador': media_avaliacoes_prestador,
            'ultimas_avaliacoes': ultimas_avaliacoes,
            'grafico_prestador': [
                pendentes_prestador,
                confirmados_prestador,
                concluidos_prestador,
                cancelados_prestador,
            ],
        })

    return render(request, 'dashboard.html', context)


@login_required
def editar_perfil(request):
    perfil = request.user.perfil

    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = PerfilForm(instance=perfil)

    return render(request, 'editar_perfil.html', {'form': form})