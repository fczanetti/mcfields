import pytest
from django.urls import reverse

from mcfields.django_assertions import assert_contains


@pytest.fixture
def resp_pag_conf_rem_video_usuario_nao_logado(client, video):
    """
    Realiza uma requisição na página de confirmação
    de remoção de vídeo com usuário não logado.
    """
    resp = client.get(reverse('videos:remocao', args=(video.pk,)))
    return resp


@pytest.fixture
def resp_pag_conf_rem_video_usuario_log_sem_perm(client_usuario_logado, video):
    """
    Realiza uma requisição na página de confirmação
    de remoção de vídeo com usuário logado sem permissão.
    """
    resp = client_usuario_logado.get(reverse('videos:remocao', args=(video.pk,)))
    return resp


@pytest.fixture
def resp_pag_conf_rem_video_usuario_log_com_perm(client_usuario_log_com_perm_remoc_video, video):
    """
    Realiza uma requisição na página de confirmação
    de remoção de vídeo com usuário logado e com permissão.
    """
    resp = client_usuario_log_com_perm_remoc_video.get(reverse('videos:remocao', args=(video.pk,)))
    return resp


def test_redirect_pag_conf_rem_usuario_nao_log(resp_pag_conf_rem_video_usuario_nao_logado):
    """
    Certifica de que, ao tentar acessar a página de confirmação de remoção com
    usuário não logado, o mesmo é redirecionado para a página de login.
    """
    assert resp_pag_conf_rem_video_usuario_nao_logado.status_code == 302
    assert resp_pag_conf_rem_video_usuario_nao_logado.url.startswith('/accounts/login/')


def test_acesso_negado_pag_conf_rem_usuario_log_sem_perm(resp_pag_conf_rem_video_usuario_log_sem_perm):
    """
    Certifica de que, ao tentar acessar a página de remoção de vídeos com
    usuário logado e sem permissão, este é redirecionado para a página de acesso negado.
    """
    assert resp_pag_conf_rem_video_usuario_log_sem_perm.status_code == 302
    assert resp_pag_conf_rem_video_usuario_log_sem_perm.url.startswith('/nao_permitido/')


def test_status_code_pag_conf_rem_video(resp_pag_conf_rem_video_usuario_log_com_perm):
    """
    Certifica de que, ao tentar acessar a página de remoção de vídeos com
    usuário logado e com permissão, esta é carregada com sucesso.
    """
    assert resp_pag_conf_rem_video_usuario_log_com_perm.status_code == 200


def test_titulo_pag_conf_rem_video(resp_pag_conf_rem_video_usuario_log_com_perm, video):
    """
    Certifica de que o título da página de confirmação de
    remoção está presente e correto.
    """
    assert_contains(resp_pag_conf_rem_video_usuario_log_com_perm, "<title>McField's - Confirmar remoção</title>")


def test_titulo_video_pag_conf_remocao(resp_pag_conf_rem_video_usuario_log_com_perm, video):
    """
    Certifica de que o título do vídeo a ser removido está
    presente na página de confirmação de remoção.
    """
    assert_contains(resp_pag_conf_rem_video_usuario_log_com_perm, video.title)


def test_botao_canc_direc_pag_detalhe_video(resp_pag_conf_rem_video_usuario_log_com_perm, video):
    """
    Certifica de que o botão de cancelar está direcionando o
    usuário para a página de detalhes do vídeo que seria removido.
    """
    assert_contains(resp_pag_conf_rem_video_usuario_log_com_perm, f'<a class="canc-removal-button" '
                                                                  f'href="{video.get_absolute_url()}">Cancelar</a>')
