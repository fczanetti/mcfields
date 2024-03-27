from datetime import date

import pytest
from django.urls import reverse
from model_bakery import baker

from mcfields.base.models import Contact
from mcfields.django_assertions import assert_contains


@pytest.fixture
def mensagens(db):
    """
    Cria algumas mensagens recebidas.
    """
    msgs = baker.make(Contact, _quantity=2)
    return msgs


@pytest.fixture
def resp_indice_mensagens_usuario_nao_logado(client):
    """
    Realiza uma requisição na página de mensagens recebidas com usuário não logado.
    """
    resp = client.get(reverse('base:indice_mensagens'))
    return resp


@pytest.fixture
def resp_indice_mensagens_usuario_log_sem_perm_view(client_usuario_logado):
    """
    Realiza uma requisição na página de mensagens recebidas com usuário logado
    sem permissão de visualização.
    """
    resp = client_usuario_logado.get(reverse('base:indice_mensagens'))
    return resp


@pytest.fixture
def resp_indice_mensag_usuario_log_com_perm_view(client_usuario_logado_com_perm_view_contact, mensagens):
    """
    Realiza uma requisição na página de índice de mensagens (contatos) recebidas
    com usuário logado e com permissão de visualização das mensagens.
    """
    resp = client_usuario_logado_com_perm_view_contact.get(reverse('base:indice_mensagens'))
    return resp


def test_redirect_indice_msgs_usuario_nao_logado(resp_indice_mensagens_usuario_nao_logado):
    """
    Certifica de que o usuário não logado, ao tentar acessar a página de índice de mensagens (contacts)
    recebidas, é redirecionado para a página de login.
    """
    assert resp_indice_mensagens_usuario_nao_logado.status_code == 302
    assert resp_indice_mensagens_usuario_nao_logado.url.startswith('/accounts/login/')


def test_redirect_indice_msgs_usuario_log_sem_perm_view(resp_indice_mensagens_usuario_log_sem_perm_view):
    """
    Certifica de que, ao tentar acessar a página de mensagens (contacts) recebidas com usuário
    logado sem permissão de visualização, este é redirecionado para a página de acesso negado.
    """
    assert resp_indice_mensagens_usuario_log_sem_perm_view.status_code == 302
    assert resp_indice_mensagens_usuario_log_sem_perm_view.url.startswith('/nao_permitido/')


def test_status_code_indice_msgs_usuario_log_com_perm_view(resp_indice_mensag_usuario_log_com_perm_view):
    """
    Certifica de que, ao tentar acessar a página de mensagens (contacts) recebidas com usuário
    logado com permissão de visualização, a página é carregada com sucesso.
    """
    assert resp_indice_mensag_usuario_log_com_perm_view.status_code == 200


def test_titulo_pag_indice_mensagens(resp_indice_mensag_usuario_log_com_perm_view):
    """
    Certifica de que o título da página de índice de mensagens recebidas está presente e correto.
    """
    assert_contains(resp_indice_mensag_usuario_log_com_perm_view, "<title>McField's - Mensagens recebidas</title>")


def test_dados_mensagens_pag_indice(resp_indice_mensag_usuario_log_com_perm_view, mensagens):
    """
    Certifica de que os dados das mensagens recebidas estão presentes na página de índice.
    """
    for msg in mensagens:
        send_date = date.strftime(msg.send_date, "%d/%m/%Y")
        assert_contains(resp_indice_mensag_usuario_log_com_perm_view, msg.name)
        assert_contains(resp_indice_mensag_usuario_log_com_perm_view, msg.subject)
        assert_contains(resp_indice_mensag_usuario_log_com_perm_view, send_date)
