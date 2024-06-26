from django.urls import path
from mcfields.servicos import views

app_name = 'servicos'
urlpatterns = [
    path('<slug:slug>', views.detalhe_servico, name='detalhe_servico'),
    path('adm/adic', views.adicionar_servico, name='adicionar'),
    path('adm/edicao/<int:id>', views.editar_servico, name='edicao'),
    path('adm/remocao/<int:id>', views.remocao_servico, name='remocao'),
]
