from django.db.models import Prefetch
from mcfields.base.models import Subject
from mcfields.videos.models import Video


def buscar_subjects_com_conteudos():
    """
    Busca os subjects (assuntos) com os vídeos relacionados. Os vídeos
    são retornados reversamente ordenados pela data de publicação/postagem.
    """
    videos = Video.objects.order_by('-post_date')
    subs = Subject.objects.order_by('order').prefetch_related(
        Prefetch('video_set', queryset=videos, to_attr='videos')).all()
    return subs
