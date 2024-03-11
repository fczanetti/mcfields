from django.shortcuts import render


def indice_videos(request):
    return render(request, 'videos/indice_videos.html')
