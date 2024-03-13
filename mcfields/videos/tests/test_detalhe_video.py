import pytest
from django.urls import reverse
from model_bakery import baker
from mcfields.django_assertions import assert_contains
from mcfields.videos.models import Video


@pytest.fixture
def video(db):
    """
    Cria um vídeo para ser exibido na página de detalhes.
    """
    vid = baker.make(Video, post_date='2024-03-12')
    return vid


@pytest.fixture
def resp_pag_det_video_usuario_nao_logado(client, video):
    """
    Realiza uma requisição na página de detalhes de vídeo com usuário não logado.
    """
    resp = client.get(reverse('videos:detalhe_video',
                              kwargs={'slug': video.slug, 'subject_slug': video.subject.slug}))
    return resp


def test_status_code_det_video_usuario_nao_logado(resp_pag_det_video_usuario_nao_logado):
    """
    Certifica de que a página de detalhes de vídeo é carregada com sucesso.
    """
    assert resp_pag_det_video_usuario_nao_logado.status_code == 200


def test_titulo_pag_detalhe_video(resp_pag_det_video_usuario_nao_logado, video):
    """
    Certifica de que o título da página de vídeos está presente e correto.
    """
    assert_contains(resp_pag_det_video_usuario_nao_logado, f"<title>McField's - {video.title}</title>")


def test_infos_video_pag_detalhe_video(resp_pag_det_video_usuario_nao_logado, video):
    """
    Certifica de que as informações do vídeo estão presentes na página de detalhes.
    """
    assert_contains(resp_pag_det_video_usuario_nao_logado, f'<h4 id="video-title">{video.title}</h4>')
    assert_contains(resp_pag_det_video_usuario_nao_logado, video.platform_id)
    assert_contains(resp_pag_det_video_usuario_nao_logado, f'<p>{video.description}</p>')
    assert_contains(resp_pag_det_video_usuario_nao_logado, f'<h4 id="video-title">{video.title}</h4>')
    assert_contains(resp_pag_det_video_usuario_nao_logado, f'<p id="video-subject">{video.subject}</p>')
    assert_contains(resp_pag_det_video_usuario_nao_logado, '<h6 id="video-post-date">12 de Março de 2024</h6>')
