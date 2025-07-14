from django.contrib import admin
from .models import (
    PerfilUsuario, Psicologo, ConexaoPsicologoPaciente, Diario, 
    CheckinEmocional, MetaTerapeutica, FraseMotivacional, 
    MensagemPrivada, Mensagem
)

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'tipo', 'telefone', 'data_criacao')
    list_filter = ('tipo', 'data_criacao')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

@admin.register(Psicologo)
class PsicologoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'registro_crp')
    search_fields = ('nome', 'email', 'registro_crp')

@admin.register(ConexaoPsicologoPaciente)
class ConexaoPsicologoPacienteAdmin(admin.ModelAdmin):
    list_display = ('psicologo', 'paciente', 'data_conexao', 'ativo')
    list_filter = ('ativo', 'data_conexao')
    search_fields = ('psicologo__username', 'paciente__username')

@admin.register(Diario)
class DiarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'humor', 'data_criacao')
    list_filter = ('humor', 'data_criacao')
    search_fields = ('usuario__username', 'texto')
    readonly_fields = ('data_criacao',)

@admin.register(CheckinEmocional)
class CheckinEmocionalAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'humor', 'data')
    list_filter = ('humor', 'data')
    search_fields = ('usuario__username',)

@admin.register(MetaTerapeutica)
class MetaTerapeuticaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'descricao', 'status', 'criado_por', 'data_criacao')
    list_filter = ('status', 'data_criacao')
    search_fields = ('usuario__username', 'descricao')

@admin.register(FraseMotivacional)
class FraseMotivacionalAdmin(admin.ModelAdmin):
    list_display = ('texto', 'ativa')
    list_filter = ('ativa',)
    search_fields = ('texto',)

@admin.register(MensagemPrivada)
class MensagemPrivadaAdmin(admin.ModelAdmin):
    list_display = ('remetente', 'destinatario', 'timestamp', 'lida')
    list_filter = ('lida', 'timestamp')
    search_fields = ('remetente__username', 'destinatario__username', 'texto')

@admin.register(Mensagem)
class MensagemAdmin(admin.ModelAdmin):
    list_display = ('remetente', 'destinatario', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('remetente__username', 'destinatario__username', 'texto')

