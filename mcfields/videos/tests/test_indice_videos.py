import pytest
from django.urls import reverse
from model_bakery import baker
from mcfields.base.models import Assunto
from mcfields.django_assertions import assert_contains
from mcfields.videos.models import Video


@pytest.fixture
def criar_assuntos(db):
    """
    Cria alguns assuntos para que vídeos sejam vinculados posteriormente.
    """
    assuntos = baker.make(Assunto, _quantity=2)
    return assuntos


@pytest.fixture
def criar_videos(criar_assuntos, db):
    """
    Cria alguns vídeos e os vincula aos assuntos criados anteriormente.
    """
    videos = []
    for assunto in criar_assuntos:
        videos.extend(baker.make(Video, _quantity=2, assunto=assunto))
    return videos


@pytest.fixture
def resp_indice_videos_usuario_nao_logado(client, db):
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


def test_titulo_assunto_indice_videos(criar_assuntos, resp_indice_videos_usuario_nao_logado):
    """
    Certifica de que o título do assunto está presente na página de índice de vídeos.
    """
    for assunto in criar_assuntos:
        assert_contains(resp_indice_videos_usuario_nao_logado, assunto.title)


def test_titulo_videos_indice_videos(criar_videos, resp_indice_videos_usuario_nao_logado):
    """
    Certifica de que os títulos dos vídeos estão presentes na página de índices.
    """
    for video in criar_videos:
        assert_contains(resp_indice_videos_usuario_nao_logado, video.title)
