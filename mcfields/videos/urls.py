from django.urls import path
from mcfields.videos import views

app_name = 'videos'
urlpatterns = [
    path('', views.indice_videos, name='indice'),
    path('adm/post', views.post_video, name='post'),
    path('adm/edicao/<int:id>', views.edicao_video, name='edicao'),
    path('<slug:subject_slug>/<slug:slug>', views.detalhe_video, name='detalhe_video'),
]
