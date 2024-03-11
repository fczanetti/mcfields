from django.shortcuts import render
from mcfields.videos import facade


def indice_videos(request):
    assuntos = facade.listar_assuntos_com_videos()
    return render(request, 'videos/indice_videos.html', {'assuntos': assuntos})
