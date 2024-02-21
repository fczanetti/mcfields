from django.urls import path
from mcfields.base import views

app_name = 'base'
urlpatterns = [
    path('', views.home, name='home'),
    path('sobre', views.sobre, name='sobre'),
]
