from django.urls import path
from mcfields.base import views

app_name = 'base'
urlpatterns = [
    path('', views.home, name='home'),
    path('politica_privacidade', views.politica_privac, name='politica_privacidade'),
    path('contato', views.contato, name='contato'),
    path('indice_mensagens', views.indice_mensagens, name='indice_mensagens'),
    path('mensagem/<int:id>', views.detalhe_mensagem, name='detalhe_mensagem'),
    path('mensagem/adm/remocao/<int:id>', views.remoc_contact, name='remoc_contact'),
    path('sobre', views.sobre, name='sobre'),
    path('assuntos', views.subjects, name='subjects'),
    path('assuntos/adm/adicao', views.adic_subject, name='adic_subject'),
    path('assuntos/adm/edicao/<int:id>', views.edic_subject, name='edic_subject'),
    path('assuntos/adm/remocao/<int:id>', views.remoc_subject, name='remoc_subject'),
    path('inscricao_concluida', views.inscricao_email, name='inscricao_email'),
    path('accounts/login/', views.UserLogin.as_view(), name='login'),
    path('nao_permitido/', views.nao_permitido, name='nao_permitido'),
]
