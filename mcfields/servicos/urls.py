from django.urls import path
from mcfields.servicos import views

app_name = 'servicos'
urlpatterns = [
    path('<slug:slug>', views.detalhe_servico, name='detalhe_servico')
]
