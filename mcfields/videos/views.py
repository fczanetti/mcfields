from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from sendgrid import SendGridAPIClient

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
            if request.POST['criar_rascunho'] == 'YES':
                criar_rascunho(
                    key=settings.SENDGRID_API_KEY,
                    titulo=request.POST['title'],
                    list_id=settings.SENDGRID_LIST_ID,
                    design_id=settings.SENDGRID_VIDEO_DESIGN_ID
                )
            return render(request, 'base/post_success.html',
                          {'titulo': request.POST['title'], 'path': path})
        else:
            return render(request, 'videos/novo_video.html', {'form': form})
    form = VideoForm()
    return render(request, 'videos/novo_video.html', {'form': form})


def criar_rascunho(key, titulo, list_id, design_id):
    """
    Cria um rascunho de email no Sendgrid.
    """
    sg = SendGridAPIClient(key)
    data = {
        'name': f'Novo vídeo: {titulo}',
        'send_to': {'list_ids': [list_id]},
        'email_config': {'design_id': design_id,
                         'suppression_group_id': settings.SUPPRESSION_GROUP_ID,
                         'sender_id': settings.SENDER_ID}
    }
    return sg.client.marketing.singlesends.post(request_body=data)
