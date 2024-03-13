from django.urls import path
from mcfields.videos import views

app_name = 'videos'
urlpatterns = [
    path('', views.indice_videos, name='indice'),
    path('<slug:subject_slug>/<slug:slug>', views.detalhe_video, name='detalhe_video'),
]
