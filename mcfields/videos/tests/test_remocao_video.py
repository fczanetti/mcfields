import pytest
from django.urls import reverse
from mcfields.django_assertions import assert_contains, assert_false
from mcfields.videos.models import Video


@pytest.fixture
def resp_remocao_video(client_usuario_log_com_perm_remoc_video, video):
    """
    Remove um vídeo cadastrado.
    """
    resp = client_usuario_log_com_perm_remoc_video.post(reverse('videos:remocao', args=(video.pk,)))
    return resp


def test_titulo_pag_remocao_concluida(resp_remocao_video):
    """
    Certifica de que o título da página de remoção concluída
    está presente.
    """
    assert_contains(resp_remocao_video, "<title>McField's - Remoção concluída</title>")


def test_pag_remocao_concluida(resp_remocao_video, video):
    """
    Certifica de que, após a remoção do vídeo, o usuário é direcionado
    para a página de remoção concluída com a mensagem informando a remoção
    e o título do vídeo removido.
    """
    assert_contains(resp_remocao_video, video.title)


def test_video_removido(resp_remocao_video, video):
    """
    Certifica de que o vídeo foi de fato removido
    do banco de dados.
    """
    exists = False
    if Video.objects.filter(id=video.pk):
        exists = True
    assert_false(exists)
