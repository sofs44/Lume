from django.shortcuts import render
from django.views import View
from .models import FraseMotivacional, Diario, CheckinEmocional, MetaTerapeutica, Mensagem
import random


class IndexView(View):
    def get(self, request, *args, **kwargs):
        frase_aleatoria = FraseMotivacional.objects.order_by('?').first()
        if frase_aleatoria:
            texto_frase = frase_aleatoria.texto
        else:
            texto_frase = "Seja bem-vindo ao Lume!"

        return render(request, 'index.html', {"frase": texto_frase})


class DiarioView(View):
    def get(self, request, *args, **kwargs):
        diarios = Diario.objects.all()
        return render(request, 'diario.html', {'diarios': diarios})


class CheckinView(View):
    def get(self, request, *args, **kwargs):
        checkins = CheckinEmocional.objects.all()
        return render(request, 'checkin.html', {'checkins': checkins})


class MetasView(View):
    def get(self, request, *args, **kwargs):
        metas = MetaTerapeutica.objects.all()
        return render(request, 'metas.html', {'metas': metas})


class ChatView(View):
    def get(self, request, *args, **kwargs):
        mensagens = Mensagem.objects.all()
        return render(request, 'chat.html', {'mensagens': mensagens})

class ConteudoView(View):
    template_name = 'conteudo.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

