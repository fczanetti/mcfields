import pytest
from django.urls import reverse

from mcfields.django_assertions import assert_contains


@pytest.fixture
def resp_indice_videos_usuario_nao_logado(client):
    """
    Realiza uma requisição na página de índice de vídeos com usuário não logado.
    """
    resp = client.get(reverse('videos:indice'))
    return resp


def test_status_code_pag_indice_videos(resp_indice_videos_usuario_nao_logado):
    """
    Certifica de que a página de índice de vídeos é carregada com sucesso.
    """
    assert resp_indice_videos_usuario_nao_logado.status_code == 200


def test_titulo_pag_indice_videos(resp_indice_videos_usuario_nao_logado):
    """
    Certifica de que o título da página de índice de vídeos está presente e correto.
    """
    assert_contains(resp_indice_videos_usuario_nao_logado, "<title>McField's - Vídeos</title>")
