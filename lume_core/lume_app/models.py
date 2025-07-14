from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class PerfilUsuario(models.Model):
    TIPO_CHOICES = [
        ('paciente', 'Paciente'),
        ('psicologo', 'Psicólogo'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='paciente')
    telefone = models.CharField(max_length=15, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_tipo_display()}"
    
    class Meta:
        verbose_name = "Perfil de Usuário"
        verbose_name_plural = "Perfis de Usuários"

@receiver(post_save, sender=User)
def criar_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.create(user=instance)

@receiver(post_save, sender=User)
def salvar_perfil_usuario(sender, instance, **kwargs):
    if hasattr(instance, 'perfil'):
        instance.perfil.save()

class Psicologo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dados_psicologo')
    nome = models.CharField(max_length=100, verbose_name="Nome do psicólogo")
    email = models.EmailField(max_length=100, unique=True, verbose_name="E-mail do psicólogo")
    registro_crp = models.CharField(max_length=20, verbose_name="Registro CRP")
    especialidades = models.TextField(blank=True, verbose_name="Especialidades")
    biografia = models.TextField(blank=True, verbose_name="Biografia")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Psicólogo"
        verbose_name_plural = "Psicólogos"

class ConexaoPsicologoPaciente(models.Model):
    psicologo = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pacientes_atribuidos')
    paciente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='psicologo_responsavel')
    data_conexao = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.psicologo.username} -> {self.paciente.username}"
    
    class Meta:
        verbose_name = "Conexão Psicólogo-Paciente"
        verbose_name_plural = "Conexões Psicólogo-Paciente"
        unique_together = ['psicologo', 'paciente']

class Diario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Diário do usuário")
    texto = models.TextField(verbose_name="Texto do diário")
    humor = models.CharField(max_length=20, verbose_name="Humor do dia", blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")

    def __str__(self):
        return f"Diário de {self.usuario.username} em {self.data_criacao.date()}"

    class Meta:
        verbose_name = "Registro de Diário"
        verbose_name_plural = "Registros de Diário"
        ordering = ['-data_criacao']

class CheckinEmocional(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Check-in do usuário")
    humor = models.CharField(max_length=50, verbose_name="Humor do usuário")
    data = models.DateField(auto_now_add=True, verbose_name="Data do check-in")

    def __str__(self):
        return f"{self.humor} em {self.data}"

    class Meta:
        verbose_name = "Check-in Emocional"
        verbose_name_plural = "Check-ins Emocionais"
        ordering = ['-data']

class MetaTerapeutica(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_progresso', 'Em Progresso'),
        ('concluida', 'Concluída'),
        ('cancelada', 'Cancelada'),
    ]
    
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metas_criadas', verbose_name="Criado por")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metas_recebidas', verbose_name="Meta para o usuário")
    descricao = models.CharField(max_length=200, verbose_name="Descrição da meta")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente', verbose_name="Status da meta")
    data_criacao = models.DateField(auto_now_add=True, verbose_name="Data de criação")
    data_conclusao = models.DateField(blank=True, null=True, verbose_name="Data de conclusão")

    def __str__(self):
        return f"Meta de {self.usuario.username}: {self.descricao}"

    class Meta:
        verbose_name = "Meta Terapêutica"
        verbose_name_plural = "Metas Terapêuticas"
        ordering = ['-data_criacao']

class FraseMotivacional(models.Model):
    texto = models.TextField(verbose_name="Frase motivacional")
    ativa = models.BooleanField(default=True, verbose_name="Ativa")

    def __str__(self):
        return self.texto[:50]

    class Meta:
        verbose_name = "Frase Motivacional"
        verbose_name_plural = "Frases Motivacionais"

class MensagemPrivada(models.Model):
    remetente = models.ForeignKey(User, related_name="mensagens_enviadas_privadas", on_delete=models.CASCADE)
    destinatario = models.ForeignKey(User, related_name="mensagens_recebidas_privadas", on_delete=models.CASCADE)
    texto = models.TextField(verbose_name="Conteúdo da mensagem")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Data e hora")
    lida = models.BooleanField(default=False, verbose_name="Lida")

    def __str__(self):
        return f"De {self.remetente.username} para {self.destinatario.username} às {self.timestamp}"

    class Meta:
        verbose_name = "Mensagem Privada"
        verbose_name_plural = "Mensagens Privadas"
        ordering = ['-timestamp']

class Mensagem(models.Model):
    remetente = models.ForeignKey(User, related_name="mensagens_enviadas", on_delete=models.CASCADE)
    destinatario = models.ForeignKey(User, related_name="mensagens_recebidas", on_delete=models.CASCADE)
    texto = models.TextField(verbose_name="Conteúdo da mensagem")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Data e hora")

    def __str__(self):
        return f"De {self.remetente.username} para {self.destinatario.username} às {self.timestamp}"

    class Meta:
        verbose_name = "Mensagem"
        verbose_name_plural = "Mensagens"
        ordering = ['-timestamp']

