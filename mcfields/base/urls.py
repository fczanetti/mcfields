from django.urls import path
from mcfields.base import views

app_name = 'base'
urlpatterns = [
    path('', views.home, name='home'),
    path('sobre', views.sobre, name='sobre'),
    path('assuntos', views.subjects, name='subjects'),
    path('assuntos/adm/adicao', views.adic_subject, name='adic_subject'),
    path('assuntos/adm/edicao/<int:id>', views.edic_subject, name='edic_subject'),
    path('assuntos/adm/remocao/<int:id>', views.remoc_subject, name='remoc_subject'),
    path('inscricao_concluida', views.inscricao_email, name='inscricao_email'),
    path('accounts/login/', views.UserLogin.as_view(), name='login'),
    path('nao_permitido/', views.nao_permitido, name='nao_permitido'),
]
