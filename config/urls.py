from django.contrib import admin
from django.urls import path
from app.views import IndexView, DiarioView, CheckinView, MetasView, ChatView
from app.views import ConteudoView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('diario/', DiarioView.as_view(), name='diario'),
    path('checkin/', CheckinView.as_view(), name='checkin'),
    path('metas/', MetasView.as_view(), name='metas'),
    path('chat/', ChatView.as_view(), name='chat'),
    path('conteudo/', ConteudoView.as_view(), name='conteudo'),
]
