from django.urls import path
from mcfields.newsletter import views


app_name = 'newsletter'
urlpatterns = [
    path('', views.indice_newsletters, name='indice_newsletters')
]
