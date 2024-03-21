from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render

from mcfields import settings
from mcfields.videos import facade
from mcfields.videos.forms import VideoForm
from mcfields.videos.models import Video


def indice_videos(request):
    assuntos = facade.listar_assuntos_com_videos()
    return render(request, 'videos/indice_videos.html', {'assuntos': assuntos})


def detalhe_video(request, slug, subject_slug):
    video = Video.objects.select_related('subject').get(slug=slug)
    return render(request, 'videos/detalhe_video.html', {'video': video})


@login_required
@permission_required('videos.add_video', login_url='/nao_permitido/')
def post_video(request):
    if request.POST:
        form = VideoForm(request.POST)
        if form.is_valid():
            form.save()
            path = request.path
            api_key = settings.SENDGRID_API_KEY
            titulo = request.POST['title']
            sg_list_id = settings.SENDGRID_LIST_ID
            sg_video_design_id = settings.SENDGRID_VIDEO_DESIGN_ID
            if request.POST['criar_rascunho'] == 'YES':
                facade.criar_rascunho(key=api_key, titulo=titulo, list_id=sg_list_id, design_id=sg_video_design_id)
            return render(request, 'base/post_success.html',
                          {'titulo': request.POST['title'], 'path': path})
        else:
            return render(request, 'videos/novo_video.html', {'form': form})
    form = VideoForm()
    return render(request, 'videos/novo_video.html', {'form': form})


@login_required
@permission_required('videos.change_video', login_url='/nao_permitido/')
def edicao_video(request, id):
    video = Video.objects.get(id=id)
    if request.method == 'POST':
        form = VideoForm(request.POST, instance=video)
        if form.is_valid():
            form.save()
            api_key = settings.SENDGRID_API_KEY
            titulo = request.POST['title']
            sg_list_id = settings.SENDGRID_LIST_ID
            sg_video_design_id = settings.SENDGRID_VIDEO_DESIGN_ID
            if request.POST['criar_rascunho'] == 'YES':
                facade.criar_rascunho(key=api_key, titulo=titulo, list_id=sg_list_id, design_id=sg_video_design_id)
            return render(request, 'base/edicao_concluida.html', {'video': video})
        else:
            return render(request, 'videos/novo_video.html', {'form': form, 'video': video})
    form = VideoForm(instance=video)
    return render(request, 'videos/novo_video.html', {'form': form, 'video': video})


@login_required
@permission_required('videos.delete_video', login_url='/nao_permitido/')
def remocao_video(request, id):
    video = Video.objects.get(id=id)
    if request.method == 'POST':
        titulo = video.title
        video.delete()
        path = request.path
        return render(request, 'base/remocao_concluida.html', {'titulo': titulo, 'path': path})
    return render(request, 'videos/confirmacao_remocao.html', {'video': video})
