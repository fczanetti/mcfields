from django.db.models import Prefetch
from sendgrid import SendGridAPIClient

from mcfields import settings
from mcfields.base.models import Subject
from mcfields.videos.models import Video


def listar_assuntos_com_videos():
    """
    Lista os assuntos com seus respectivos vídeos relacionados.
    """
    videos = Video.objects.order_by('-post_date')
    return Subject.objects.order_by('order').prefetch_related(
        Prefetch('video_set', queryset=videos, to_attr='videos')).all()


def criar_rascunho(key, titulo, list_id, design_id):
    """
    Cria um rascunho de email no SendGrid após a postagem ou edição de um vídeo. O rascunho
    só é criado se o usuário assinalar a opção de criar rascunho.
    :param key: SENDGRID_API_KEY;
    :param titulo: Título do vídeo postado ou editado;
    :param list_id: ID da lista de contatos para os quais o email será enviado (SENDGRID_LIST_ID);
    :param design_id: ID do modelo de email criado para vídeos no SendGrid (SENDGRID_VIDEO_DESIGN_ID);
    :return: Requisição no site do SendGrid criando o rascunho.
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
