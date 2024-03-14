import pytest
from django.urls import reverse
from model_bakery import baker
from mcfields.django_assertions import assert_contains, assert_not_contains
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


@pytest.fixture
def resp_pag_det_video_usuario_log_sem_perm_edic(client_usuario_logado, video):
    """
    Realiza uma requisição na página de detalhes de vídeo com
    usuário logado sem permissão de edição.
    """
    resp = client_usuario_logado.get(reverse('videos:detalhe_video',
                                             kwargs={'slug': video.slug, 'subject_slug': video.subject.slug}))
    return resp


@pytest.fixture
def resp_pag_det_video_usuario_log_com_perm_edic(client_usuario_log_com_perm_edic_video, video):
    """
    Realiza uma requisição na página de detalhes de vídeo com
    usuário logado com permissão de edição.
    """
    resp = client_usuario_log_com_perm_edic_video.get(reverse('videos:detalhe_video',
                                                              kwargs={'slug': video.slug,
                                                                      'subject_slug': video.subject.slug}))
    return resp


@pytest.fixture
def resp_pag_det_video_usuario_log_sem_perm_remocao(client_usuario_logado, video):
    """
    Realiza uma requisição na página de detalhes de vídeo com
    usuário logado sem permissão de remoção.
    """
    resp = client_usuario_logado.get(reverse('videos:detalhe_video',
                                             kwargs={'slug': video.slug, 'subject_slug': video.subject.slug}))
    return resp


@pytest.fixture
def resp_pag_det_video_usuario_log_com_perm_remocao(client_usuario_log_com_perm_remoc_video, video):
    """
    Realiza uma requisição na página de detalhes de vídeo com
    usuário logado com permissão de edição.
    """
    resp = client_usuario_log_com_perm_remoc_video.get(reverse('videos:detalhe_video',
                                                               kwargs={'slug': video.slug,
                                                                       'subject_slug': video.subject.slug}))
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


def test_bot_edicao_nao_disp_usuario_nao_logado(resp_pag_det_video_usuario_nao_logado):
    """
    Certifica de que o botão de edição de vídeo não está
    presente na página para o usuário não logado.
    """
    assert_not_contains(resp_pag_det_video_usuario_nao_logado, 'Editar')


def test_bot_edicao_nao_disp_usuario_log_sem_perm(resp_pag_det_video_usuario_log_sem_perm_edic):
    """
    Certifica de que o botão de edição de vídeo não está
    presente na página para o usuário logado sem permissão.
    """
    assert_not_contains(resp_pag_det_video_usuario_log_sem_perm_edic, 'Editar')


def test_bot_edicao_disp_usuario_logado_com_perm(resp_pag_det_video_usuario_log_com_perm_edic):
    """
    Certifica de que o botão de edição de vídeo está
    presente na página para o usuário logado com permissão.
    """
    assert_contains(resp_pag_det_video_usuario_log_com_perm_edic, 'Editar')


def test_botao_remocao_indisp_usuario_nao_logado(resp_pag_det_video_usuario_nao_logado, video):
    """
    Certifica de que o botão de remoção de vídeos não está
    disponível para o usuário não logado.
    """
    assert_not_contains(resp_pag_det_video_usuario_nao_logado, f'<a id="video-removal-link" '
                                                               f'href="{video.get_removal_url()}">Remover</a>')


def test_botao_remocao_indisp_usuario_logado_sem_perm(resp_pag_det_video_usuario_log_sem_perm_remocao, video):
    """
    Certifica de que o botão de remoção de vídeos não está
    disponível para o usuário logado sem permissão de remoção.
    """
    assert_not_contains(resp_pag_det_video_usuario_log_sem_perm_remocao,
                        f'<a id="video-removal-link" href="{video.get_removal_url()}">Remover</a>')


def test_botao_remocao_disp_usuario_logado_com_perm(resp_pag_det_video_usuario_log_com_perm_remocao, video):
    """
    Certifica de que o botão de remoção de vídeos está
    disponível para o usuário logado com permissão de remoção.
    """
    assert_contains(resp_pag_det_video_usuario_log_com_perm_remocao,
                    f'<a id="video-removal-link" href="{video.get_removal_url()}">Remover</a>')
