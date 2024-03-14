import pytest
from django.urls import reverse
from model_bakery import baker
from mcfields.base.models import Subject
from mcfields.django_assertions import assert_contains
from mcfields.videos.models import Video


@pytest.fixture
def criar_subjects(db):
    """
    Cria alguns assuntos para que vídeos sejam vinculados posteriormente.
    """
    subjects = baker.make(Subject, _quantity=2)
    return subjects


@pytest.fixture
def criar_videos(criar_subjects, db):
    """
    Cria alguns vídeos e os vincula aos assuntos criados anteriormente.
    """
    videos = []
    for subject in criar_subjects:
        videos.extend(baker.make(Video, _quantity=2, subject=subject))
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


def test_titulo_assunto_indice_videos(criar_subjects, resp_indice_videos_usuario_nao_logado):
    """
    Certifica de que o título do assunto está presente na página de índice de vídeos.
    """
    for subject in criar_subjects:
        assert_contains(resp_indice_videos_usuario_nao_logado, subject.title)


def test_titulo_videos_indice_videos(criar_videos, resp_indice_videos_usuario_nao_logado):
    """
    Certifica de que os títulos dos vídeos estão presentes na página de índices.
    """
    for video in criar_videos:
        assert_contains(resp_indice_videos_usuario_nao_logado, video.title)


def test_links_videos_indice_videos(criar_videos, resp_indice_videos_usuario_nao_logado):
    """
    Certifica de que os links dos vídeos estão presentes na página de índices.
    """
    for video in criar_videos:
        assert_contains(resp_indice_videos_usuario_nao_logado, video.get_absolute_url())
