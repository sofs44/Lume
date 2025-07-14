from django.urls import path
from . import views

urlpatterns = [
    # Páginas principais
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro_view, name='registro'),
    
    # Painéis
    path('painel-psicologo/', views.painel_psicologo, name='painel_psicologo'),
    path('painel-paciente/', views.painel_paciente, name='painel_paciente'),
    
    # Funcionalidades do psicólogo
    path('psicologo/adicionar-paciente/', views.adicionar_paciente, name='adicionar_paciente'),
    path('psicologo/ficha-paciente/<int:paciente_id>/', views.ficha_paciente, name='ficha_paciente'),
    path('psicologo/mensagens/', views.mensagens_privadas, name='mensagens_psicologo'),
    path('psicologo/mensagens/<int:destinatario_id>/', views.mensagens_privadas, name='mensagens_psicologo_conversa'),
    
    # Funcionalidades do paciente
    path('paciente/salvar-humor/', views.salvar_humor, name='salvar_humor'),
    path('paciente/mensagens/', views.mensagens_privadas, name='mensagens_paciente'),
    path('paciente/mensagens/<int:destinatario_id>/', views.mensagens_privadas, name='mensagens_paciente_conversa'),
    
    # Páginas de ferramentas (mantidas para compatibilidade)
    path('chat/', views.chat, name='chat'),
    path('conteudo/', views.conteudo, name='conteudo'),
    path('metas/', views.metas, name='metas'),
    path('diario/', views.diario, name='diario'),
]

