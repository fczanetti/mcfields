from django.urls import path
from mcfields.newsletter import views


app_name = 'newsletter'
urlpatterns = [
    path('', views.indice_newsletters, name='indice_newsletters'),
    path('<slug:slug>', views.detalhe_newsletter, name='detalhe_newsletter'),
    path('adm/post', views.post_newsletter, name='post'),
]
