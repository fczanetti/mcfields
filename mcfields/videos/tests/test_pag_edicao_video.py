import pytest
from django.urls import reverse
from mcfields.django_assertions import assert_contains


@pytest.fixture
def resp_pag_edicao_video_usuario_nao_logado(client, video):
    """
    Cria uma requisição na página de edição de vídeos com usuário não logado.
    """
    resp = client.get(reverse('videos:edicao', args=(video.pk,)))
    return resp


@pytest.fixture
def resp_pag_edicao_video_usuario_log_sem_perm(client_usuario_logado, video):
    """
    Cria uma requisição na página de edição de vídeos com usuário logado
    sem permissão de edição.
    """
    resp = client_usuario_logado.get(reverse('videos:edicao', args=(video.pk,)))
    return resp


@pytest.fixture
def resp_pag_edicao_video_usuario_logado_com_perm(client_usuario_log_com_perm_edic_video, video):
    """
    Cria uma requisição na página de edição de vídeos com usuário logado
    e com permissão.
    """
    resp = client_usuario_log_com_perm_edic_video.get(reverse('videos:edicao', args=(video.pk,)))
    return resp


def test_titulo_pag_edicao_video(resp_pag_edicao_video_usuario_logado_com_perm):
    """
    Certifica de que o título da página informa da edição de um vídeo existente.
    """
    assert_contains(resp_pag_edicao_video_usuario_logado_com_perm, "<title>McField's - Edição de vídeo</title>")


def test_redirect_usuario_nao_logado(resp_pag_edicao_video_usuario_nao_logado):
    """
    Certifica de que, ao tentar acessar a página de edição de vídeos com
    usuário não logado, o mesmo é redirecionado para a página de login.
    """
    assert resp_pag_edicao_video_usuario_nao_logado.status_code == 302
    assert resp_pag_edicao_video_usuario_nao_logado.url.startswith('/accounts/login/')


def test_acesso_negado_usuario_log_sem_perm(resp_pag_edicao_video_usuario_log_sem_perm):
    """
    Certifica de que, ao tentar acessar a página de edição de vídeos com
    usuário logado sem permissão, o mesmo é redirecionado para a página de acesso negado.
    """
    assert resp_pag_edicao_video_usuario_log_sem_perm.status_code == 302
    assert resp_pag_edicao_video_usuario_log_sem_perm.url.startswith('/nao_permitido/')


def test_status_code_pag_edicao_video(resp_pag_edicao_video_usuario_logado_com_perm):
    """
    Certifica de que, ao tentar acessar a página de edição de vídeo com usuário logado
    e com permissão, esta é carregada com sucesso.
    """
    assert resp_pag_edicao_video_usuario_logado_com_perm.status_code == 200


def test_infos_video_pag_edicao(resp_pag_edicao_video_usuario_logado_com_perm, video):
    """
    Certifica de que as informações do vídeo estão presentes na página de edição.
    """
    assert_contains(resp_pag_edicao_video_usuario_logado_com_perm, f'<input type="text" name="title" '
                                                                   f'value="{video.title}" maxlength="64" '
                                                                   f'required id="id_title">')
    assert_contains(resp_pag_edicao_video_usuario_logado_com_perm, video.description)
    assert_contains(resp_pag_edicao_video_usuario_logado_com_perm, video.subject)
    assert_contains(resp_pag_edicao_video_usuario_logado_com_perm, video.platform_id)
    assert_contains(resp_pag_edicao_video_usuario_logado_com_perm, video.slug)


def test_titulo_form(resp_pag_edicao_video_usuario_logado_com_perm, video):
    """
    Certifica de que o título do formulário está presente e
    indicando a edição de um vídeo existente.
    """
    assert_contains(resp_pag_edicao_video_usuario_logado_com_perm, f'<h1 class="form-title">Edição do Vídeo '
                                                                   f'"{video.title}"</h1>')
