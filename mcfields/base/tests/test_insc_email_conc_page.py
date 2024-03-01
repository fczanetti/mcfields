from unittest.mock import Mock
import pytest
from django.urls import reverse

from mcfields.base import views
from mcfields.django_assertions import assert_contains


@pytest.fixture
def resp_inscricao_email_concluida(client):
    """
    Realiza uma requisição post no formulário de email.
    """
    views.cadastrar_email = Mock()
    resp = client.post(reverse('base:inscricao_email'), {'email': 'teste@teste.com'})
    return resp


def test_status_code_insc_email_conc(resp_inscricao_email_concluida):
    """
    Certifica de que a página de inscrição de email concluída foi carregada com sucesso.
    """
    assert resp_inscricao_email_concluida.status_code == 200


def test_titulo_pagina_insc_email_conc(resp_inscricao_email_concluida):
    """
    Certifica de que o título da página de inscrição de email concluída está presente e correto.
    """
    assert_contains(resp_inscricao_email_concluida, "<title>McField's - Inscrição concluída</title>")


def test_message_success_email_subscription(resp_inscricao_email_concluida):
    """
    Certifica de que a mensagem de email inscrito com sucesso é apresentada e contém o email cadastrado.
    """
    assert_contains(resp_inscricao_email_concluida,
                    f'O email <strong>{resp_inscricao_email_concluida.wsgi_request.POST["email"]}</strong> foi '
                    f'cadastrado com sucesso.')


def test_inscricao_email_concluida(client):
    """
    Certifica de que a função de cadastrar_email é chamada ao realizar uma inscrição.
    """
    views.cadastrar_email = Mock()
    client.post(reverse('base:inscricao_email'), {'email': 'fabio@hotmail.com'})
    views.cadastrar_email.assert_called_once()
