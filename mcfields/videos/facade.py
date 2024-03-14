from django.db.models import Prefetch
from mcfields.base.models import Subject
from mcfields.videos.models import Video


def listar_assuntos_com_videos():
    """
    Lista os assuntos com seus respectivos vídeos relacionados.
    """
    videos = Video.objects.order_by('-post_date')
    return Subject.objects.order_by('order').prefetch_related(
        Prefetch('video_set', queryset=videos, to_attr='videos')).all()
