import pytest
from django.urls import reverse

from mcfields.django_assertions import assert_contains, assert_not_contains


@pytest.fixture
def resp_pag_det_mensag_usuario_nao_log(client, mensagem):
    """
    Realiza uma requisição na página de detalhes de uma mensagem recebida
    com usuário não logado.
    """
    resp = client.get(reverse('base:detalhe_mensagem', args=(mensagem.pk,)))
    return resp


@pytest.fixture
def resp_pag_det_mensag_usuario_log_sem_perm_view(client_usuario_logado, mensagem):
    """
    Realiza uma requisição na página de detalhes de uma mensagem recebida
    com usuário logado sem permissão de visualização de mensagens (contacts).
    """
    resp = client_usuario_logado.get(reverse('base:detalhe_mensagem', args=(mensagem.pk,)))
    return resp


@pytest.fixture
def resp_pag_det_mensag_usuario_log_com_perm_view(client_usuario_logado_com_perm_view_contact, mensagem):
    """
    Realiza uma requisição na página de detalhes de uma mensagem recebida
    com usuário logado com permissão de visualização de mensagens (contacts).
    """
    resp = client_usuario_logado_com_perm_view_contact.get(reverse('base:detalhe_mensagem',
                                                                   args=(mensagem.pk,)))
    return resp


@pytest.fixture
def resp_pag_det_mensag_usuario_log_com_perm_view_e_remoc(
        client_usuario_logado_com_perm_view_e_remoc_contact, mensagem):
    """
    Realiza uma requisição na página de detalhes de uma mensagem recebida
    com usuário logado com permissão de visualização e remoção de mensagens (contacts).
    """
    resp = client_usuario_logado_com_perm_view_e_remoc_contact.get(reverse('base:detalhe_mensagem',
                                                                   args=(mensagem.pk,)))
    return resp


def test_redirect_detalhe_mensagem_usuario_nao_log(resp_pag_det_mensag_usuario_nao_log):
    """
    Certifica de que, ao tentar acessar a página de detalhes de mensagem com usuário
    não logado, este é redirecionado para a página de login.
    """
    assert resp_pag_det_mensag_usuario_nao_log.status_code == 302
    assert resp_pag_det_mensag_usuario_nao_log.url.startswith('/accounts/login/')


def test_redirect_detalhe_mensag_usuario_log_sem_perm_view(resp_pag_det_mensag_usuario_log_sem_perm_view):
    """
    Certifica de que, ao tentar acessar a página de detalhes de mensagem com usuário
    logado sem permissão de visualização, este é redirecionado para a página de login.
    """
    assert resp_pag_det_mensag_usuario_log_sem_perm_view.status_code == 302
    assert resp_pag_det_mensag_usuario_log_sem_perm_view.url.startswith('/nao_permitido/')


def test_status_code_det_mensag_usuario_log_com_perm_view(resp_pag_det_mensag_usuario_log_com_perm_view):
    """
    Certifica de que, ao tentar acessar a página de detalhes de mensagem com usuário
    logado com permissão de visualização, a página é carregada com sucesso.
    """
    assert resp_pag_det_mensag_usuario_log_com_perm_view.status_code == 200


def test_titulo_pag_detalhe_mensagem(resp_pag_det_mensag_usuario_log_com_perm_view):
    """
    Certifica de que o título da página de detalhes de mensagem está presente e correto.
    """
    assert_contains(resp_pag_det_mensag_usuario_log_com_perm_view, "<title>McField's - Mensagem recebida</title>")


def test_infos_mensagem_pag_detalhes(resp_pag_det_mensag_usuario_log_com_perm_view, mensagem):
    """
    Certifica de que as informações da mensagem estão presentes na página de detalhes.
    """
    assert_contains(resp_pag_det_mensag_usuario_log_com_perm_view, f'<h1 class="title">Mensagem de '
                                                                   f'{mensagem.name}</h1>')
    assert_contains(resp_pag_det_mensag_usuario_log_com_perm_view, f'<a id="reply-email" href="mailto:{mensagem.email}?'
                                                                   f'subject={mensagem.subject}">{mensagem.email}</a>')
    assert_contains(resp_pag_det_mensag_usuario_log_com_perm_view, f'<h5 id="message_subject">{mensagem.subject}</h5>')
    assert_contains(resp_pag_det_mensag_usuario_log_com_perm_view, f'<div id="message_content">'
                                                                   f'<p>{mensagem.message}</p></div>')


def test_botao_remoc_mensag_indisp_usuario_sem_perm(resp_pag_det_mensag_usuario_log_com_perm_view, mensagem):
    """
    Certifica de que o botão de remoção de mensagem não está presente para
    o usuário que não tem permissão de remoção.
    """
    assert_not_contains(resp_pag_det_mensag_usuario_log_com_perm_view, f'<a class="removal-link" '
                                                                       f'href="{mensagem.get_removal_url()}">'
                                                                       f'Remover</a>')


def test_botao_remoc_mensag_disp_usuario_com_perm(resp_pag_det_mensag_usuario_log_com_perm_view_e_remoc, mensagem):
    """
    Certifica de que o botão de remoção de mensagem está presente para
    o usuário que tem permissão de remoção.
    """
    assert_contains(resp_pag_det_mensag_usuario_log_com_perm_view_e_remoc, f'<a class="removal-link" '
                                                                           f'href="{mensagem.get_removal_url()}">'
                                                                           f'Remover</a>')
