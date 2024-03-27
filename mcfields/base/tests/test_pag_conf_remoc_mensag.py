import pytest
from django.urls import reverse

from mcfields.django_assertions import assert_contains


@pytest.fixture
def resp_pag_conf_remoc_mensag_usuario_nao_log(client, mensagem):
    """
    Realiza uma requisição na página de confirmação de remoção de mensagem (contacts)
    com usuário não logado.
    """
    resp = client.get(reverse('base:remoc_contact', args=(mensagem.pk,)))
    return resp


@pytest.fixture
def resp_pag_conf_remoc_mensag_usuario_log_sem_perm(client_usuario_logado, mensagem):
    """
    Realiza uma requisição na página de confirmação de remoção de mensagem (contacts)
    com usuário logado sem permissão de remoção.
    """
    resp = client_usuario_logado.get(reverse('base:remoc_contact', args=(mensagem.pk,)))
    return resp


@pytest.fixture
def resp_pag_conf_remoc_mensag_usuario_log_com_perm(client_usuario_logado_com_perm_remoc_contact, mensagem):
    """
    Realiza uma requisição na página de confirmação de remoção de mensagem (contacts)
    com usuário logado e com permissão de remoção de mensagens (contacts).
    """
    resp = client_usuario_logado_com_perm_remoc_contact.get(
        reverse('base:remoc_contact', args=(mensagem.pk,)))
    return resp


def test_redirect_pag_remoc_mensag_usuario_nao_log(resp_pag_conf_remoc_mensag_usuario_nao_log):
    """
    Certifica de que, ao tentar acessar a página de confirmação de remoção de mensagem
    com usuário não logado, este é redirecionado para a página de login.
    """
    assert resp_pag_conf_remoc_mensag_usuario_nao_log.status_code == 302
    assert resp_pag_conf_remoc_mensag_usuario_nao_log.url.startswith('/accounts/login/')


def test_redirect_pag_remoc_mensag_usuario_log_sem_perm(resp_pag_conf_remoc_mensag_usuario_log_sem_perm):
    """
    Certifica de que, ao tentar acessar a página de confirmação de remoção de mensagem
    com usuário logado sem permissão de remoção, este é redirecionado para a página de acesso negado.
    """
    assert resp_pag_conf_remoc_mensag_usuario_log_sem_perm.status_code == 302
    assert resp_pag_conf_remoc_mensag_usuario_log_sem_perm.url.startswith('/nao_permitido/')


def test_status_code_pag_remoc_mensag_usuario_log_com_perm(resp_pag_conf_remoc_mensag_usuario_log_com_perm):
    """
    Certifica de que, ao tentar acessar a página de confirmação de remoção de mensagem
    com usuário logado com permissão de remoção, a página é carregada com sucesso.
    """
    assert resp_pag_conf_remoc_mensag_usuario_log_com_perm.status_code == 200


def test_titulo_pag_conf_remocao(resp_pag_conf_remoc_mensag_usuario_log_com_perm):
    """
    Certifica de que o título da página de confirmação de remoção está presente.
    """
    assert_contains(resp_pag_conf_remoc_mensag_usuario_log_com_perm, "<title>McField's - Confirmar remoção</title>")


def test_nome_mensagem_pag_conf_remocao(resp_pag_conf_remoc_mensag_usuario_log_com_perm, mensagem):
    """
    Certifica de que o nome do remetente da mensagem está disponível na página de confirmação
     de remoção desta.
    """
    assert_contains(resp_pag_conf_remoc_mensag_usuario_log_com_perm, mensagem.name)


def test_botao_cancelar_pag_conf_remocao(resp_pag_conf_remoc_mensag_usuario_log_com_perm, mensagem):
    """
    Certifica de que o botão de cancelar remoção está presente e direcionando para página
    de detalhes da newlstter que seria removida.
    """
    assert_contains(resp_pag_conf_remoc_mensag_usuario_log_com_perm, f'<a class="canc-removal-button" '
                                                                     f'href="{mensagem.get_absolute_url()}">'
                                                                     f'Cancelar</a>')
