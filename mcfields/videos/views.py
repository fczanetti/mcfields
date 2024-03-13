from django.shortcuts import render
from mcfields.videos import facade
from mcfields.videos.models import Video


def indice_videos(request):
    assuntos = facade.listar_assuntos_com_videos()
    return render(request, 'videos/indice_videos.html', {'assuntos': assuntos})


def detalhe_video(request, slug, subject_slug):
    video = Video.objects.select_related('subject').get(slug=slug)
    return render(request, 'videos/detalhe_video.html', {'video': video})
