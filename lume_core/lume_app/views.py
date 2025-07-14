from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import Q, Count
from django.utils import timezone
from datetime import datetime, timedelta
import json
import random

from .models import (
    FraseMotivacional, Diario, CheckinEmocional, MetaTerapeutica, 
    Mensagem, MensagemPrivada, PerfilUsuario, Psicologo, ConexaoPsicologoPaciente
)
from .forms import RegistroForm, LoginForm

def index(request):
    """Página inicial com frase motivacional"""
    try:
        frase = FraseMotivacional.objects.filter(ativa=True).order_by('?').first()
        frase_texto = frase.texto if frase else "Cada dia é uma nova oportunidade de crescimento e superação."
    except:
        frase_texto = "Cada dia é uma nova oportunidade de crescimento e superação."
    
    context = {
        'frase': frase_texto,
    }
    return render(request, 'index.html', context)

def login_view(request):
    """View de login com redirecionamento baseado no tipo de usuário"""
    if request.user.is_authenticated:
        return redirect_by_user_type(request.user)
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo, {user.first_name}!')
                return redirect_by_user_type(user)
            else:
                messages.error(request, 'Nome de usuário ou senha incorretos.')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

def registro_view(request):
    """View de registro com seleção de tipo de usuário"""
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Conta criada com sucesso! Faça login para continuar.')
            return redirect('login')
    else:
        form = RegistroForm()
    
    return render(request, 'registro.html', {'form': form})

def redirect_by_user_type(user):
    """Redireciona usuário baseado no tipo"""
    try:
        if user.perfil.tipo == 'psicologo':
            return redirect('painel_psicologo')
        else:
            return redirect('painel_paciente')
    except:
        return redirect('painel_paciente')

@login_required
def painel_psicologo(request):
    """Painel do psicólogo"""
    if not hasattr(request.user, 'perfil') or request.user.perfil.tipo != 'psicologo':
        messages.error(request, 'Acesso negado. Você não é um psicólogo.')
        return redirect('index')
    
    # Buscar pacientes atribuídos
    pacientes = ConexaoPsicologoPaciente.objects.filter(
        psicologo=request.user, 
        ativo=True
    ).select_related('paciente')
    
    # Buscar pacientes disponíveis para atribuição
    pacientes_atribuidos_ids = pacientes.values_list('paciente_id', flat=True)
    pacientes_disponiveis = User.objects.filter(
        perfil__tipo='paciente'
    ).exclude(
        id__in=pacientes_atribuidos_ids
    )
    
    # Estatísticas gerais
    total_checkins = CheckinEmocional.objects.filter(
        usuario__in=[p.paciente for p in pacientes],
        data__gte=timezone.now().date() - timedelta(days=7)
    ).count()
    
    total_diarios = Diario.objects.filter(
        usuario__in=[p.paciente for p in pacientes]
    ).count()
    
    metas_concluidas = MetaTerapeutica.objects.filter(
        criado_por=request.user,
        status='concluida'
    ).count()
    
    context = {
        'pacientes': pacientes,
        'pacientes_disponiveis': pacientes_disponiveis,
        'total_checkins': total_checkins,
        'total_diarios': total_diarios,
        'metas_concluidas': metas_concluidas,
    }
    return render(request, 'painel_psicologo.html', context)

@login_required
def painel_paciente(request):
    """Painel do paciente"""
    if hasattr(request.user, 'perfil') and request.user.perfil.tipo == 'psicologo':
        return redirect('painel_psicologo')
    
    # Buscar psicólogo responsável
    try:
        conexao = ConexaoPsicologoPaciente.objects.get(
            paciente=request.user, 
            ativo=True
        )
        psicologo_responsavel = conexao.psicologo
    except ConexaoPsicologoPaciente.DoesNotExist:
        psicologo_responsavel = None
    
    # Estatísticas do paciente
    total_diarios = Diario.objects.filter(usuario=request.user).count()
    
    # Check-ins da semana
    inicio_semana = timezone.now().date() - timedelta(days=7)
    checkins_semana = CheckinEmocional.objects.filter(
        usuario=request.user,
        data__gte=inicio_semana
    ).count()
    checkins_semana_percent = min((checkins_semana / 7) * 100, 100)
    
    # Metas
    metas_ativas = MetaTerapeutica.objects.filter(
        usuario=request.user,
        status__in=['pendente', 'em_progresso']
    ).count()
    
    metas_concluidas = MetaTerapeutica.objects.filter(
        usuario=request.user,
        status='concluida'
    ).count()
    
    total_metas = MetaTerapeutica.objects.filter(usuario=request.user).count()
    metas_concluidas_percent = (metas_concluidas / total_metas * 100) if total_metas > 0 else 0
    
    # Diários da semana
    diarios_semana = Diario.objects.filter(
        usuario=request.user,
        data_criacao__gte=timezone.now() - timedelta(days=7)
    ).count()
    diarios_semana_percent = min((diarios_semana / 7) * 100, 100)
    
    # Mensagens recentes
    mensagens_recentes = []
    if psicologo_responsavel:
        mensagens_recentes = MensagemPrivada.objects.filter(
            Q(remetente=request.user, destinatario=psicologo_responsavel) |
            Q(remetente=psicologo_responsavel, destinatario=request.user)
        ).order_by('-timestamp')[:3]
    
    # Frase motivacional
    try:
        frase = FraseMotivacional.objects.filter(ativa=True).order_by('?').first()
        frase_motivacional = frase.texto if frase else "Você é mais forte do que imagina."
    except:
        frase_motivacional = "Você é mais forte do que imagina."
    
    context = {
        'psicologo_responsavel': psicologo_responsavel,
        'total_diarios': total_diarios,
        'checkins_semana': checkins_semana,
        'checkins_semana_percent': checkins_semana_percent,
        'metas_ativas': metas_ativas,
        'metas_concluidas': metas_concluidas,
        'total_metas': total_metas,
        'metas_concluidas_percent': metas_concluidas_percent,
        'diarios_semana': diarios_semana,
        'diarios_semana_percent': diarios_semana_percent,
        'mensagens_recentes': mensagens_recentes,
        'frase_motivacional': frase_motivacional,
    }
    return render(request, 'painel_paciente.html', context)

@login_required
@require_POST
def adicionar_paciente(request):
    """Adicionar paciente ao psicólogo"""
    if not hasattr(request.user, 'perfil') or request.user.perfil.tipo != 'psicologo':
        return JsonResponse({'success': False, 'message': 'Acesso negado.'})
    
    paciente_id = request.POST.get('paciente_id')
    if not paciente_id:
        return JsonResponse({'success': False, 'message': 'ID do paciente não fornecido.'})
    
    try:
        paciente = User.objects.get(id=paciente_id, perfil__tipo='paciente')
        
        # Verificar se já existe conexão
        if ConexaoPsicologoPaciente.objects.filter(
            psicologo=request.user, 
            paciente=paciente
        ).exists():
            return JsonResponse({'success': False, 'message': 'Paciente já está atribuído a você.'})
        
        # Criar conexão
        ConexaoPsicologoPaciente.objects.create(
            psicologo=request.user,
            paciente=paciente
        )
        
        return JsonResponse({'success': True, 'message': 'Paciente adicionado com sucesso.'})
        
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Paciente não encontrado.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': 'Erro interno do servidor.'})

@login_required
@require_POST
def salvar_humor(request):
    """Salvar humor do paciente"""
    try:
        data = json.loads(request.body)
        mood = data.get('mood')
        
        if not mood:
            return JsonResponse({'success': False, 'message': 'Humor não fornecido.'})
        
        # Verificar se já existe check-in hoje
        hoje = timezone.now().date()
        checkin, created = CheckinEmocional.objects.get_or_create(
            usuario=request.user,
            data=hoje,
            defaults={'humor': mood}
        )
        
        if not created:
            checkin.humor = mood
            checkin.save()
        
        return JsonResponse({'success': True, 'message': 'Humor salvo com sucesso.'})
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': 'Erro ao salvar humor.'})

def logout_view(request):
    """Logout do usuário"""
    logout(request)
    messages.success(request, 'Você foi desconectado com sucesso.')
    return redirect('index')

@login_required
def chat(request):
    """Página de chat"""
    return render(request, 'chat.html')

@login_required
def conteudo(request):
    """Página de conteúdo terapêutico"""
    return render(request, 'conteudo.html')

@login_required
def metas(request):
    """Página de metas e check-in"""
    return render(request, 'metas.html')

@login_required
def diario(request):
    """Página de diário"""
    return render(request, 'diario.html')

@login_required
def ficha_paciente(request, paciente_id):
    """Ficha detalhada do paciente para psicólogos"""
    if not hasattr(request.user, 'perfil') or request.user.perfil.tipo != 'psicologo':
        return HttpResponse('Acesso negado', status=403)
    
    # Verificar se o paciente está atribuído ao psicólogo
    try:
        conexao = ConexaoPsicologoPaciente.objects.get(
            psicologo=request.user,
            paciente_id=paciente_id,
            ativo=True
        )
        paciente = conexao.paciente
    except ConexaoPsicologoPaciente.DoesNotExist:
        return HttpResponse('Paciente não encontrado', status=404)
    
    # Buscar dados do paciente
    diarios = Diario.objects.filter(usuario=paciente).order_by('-data_criacao')[:10]
    checkins = CheckinEmocional.objects.filter(usuario=paciente).order_by('-data')[:10]
    metas = MetaTerapeutica.objects.filter(usuario=paciente).order_by('-data_criacao')[:10]
    
    context = {
        'paciente': paciente,
        'diarios': diarios,
        'checkins': checkins,
        'metas': metas,
    }
    
    return render(request, 'ficha_paciente.html', context)

@login_required
def mensagens_privadas(request, destinatario_id=None):
    """Sistema de mensagens privadas"""
    if destinatario_id:
        destinatario = get_object_or_404(User, id=destinatario_id)
        
        # Verificar se há conexão entre psicólogo e paciente
        if request.user.perfil.tipo == 'psicologo':
            if not ConexaoPsicologoPaciente.objects.filter(
                psicologo=request.user,
                paciente=destinatario,
                ativo=True
            ).exists():
                messages.error(request, 'Você não tem permissão para conversar com este usuário.')
                return redirect('painel_psicologo')
        else:
            if not ConexaoPsicologoPaciente.objects.filter(
                psicologo=destinatario,
                paciente=request.user,
                ativo=True
            ).exists():
                messages.error(request, 'Você não tem permissão para conversar com este usuário.')
                return redirect('painel_paciente')
        
        # Buscar mensagens da conversa
        mensagens = MensagemPrivada.objects.filter(
            Q(remetente=request.user, destinatario=destinatario) |
            Q(remetente=destinatario, destinatario=request.user)
        ).order_by('timestamp')
        
        # Marcar mensagens como lidas
        MensagemPrivada.objects.filter(
            remetente=destinatario,
            destinatario=request.user,
            lida=False
        ).update(lida=True)
        
        if request.method == 'POST':
            texto = request.POST.get('texto', '').strip()
            if texto:
                MensagemPrivada.objects.create(
                    remetente=request.user,
                    destinatario=destinatario,
                    texto=texto
                )
                return redirect('mensagens_privadas', destinatario_id=destinatario_id)
        
        context = {
            'destinatario': destinatario,
            'mensagens': mensagens,
        }
        return render(request, 'mensagens_privadas.html', context)
    
    else:
        # Lista de conversas
        if request.user.perfil.tipo == 'psicologo':
            # Psicólogo vê seus pacientes
            conexoes = ConexaoPsicologoPaciente.objects.filter(
                psicologo=request.user,
                ativo=True
            ).select_related('paciente')
            contatos = [c.paciente for c in conexoes]
        else:
            # Paciente vê seu psicólogo
            try:
                conexao = ConexaoPsicologoPaciente.objects.get(
                    paciente=request.user,
                    ativo=True
                )
                contatos = [conexao.psicologo]
            except ConexaoPsicologoPaciente.DoesNotExist:
                contatos = []
        
        context = {
            'contatos': contatos,
        }
        return render(request, 'lista_mensagens.html', context)

