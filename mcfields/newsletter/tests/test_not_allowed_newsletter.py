import pytest
from django.urls import reverse

from mcfields.django_assertions import assert_contains


@pytest.fixture
def resp_not_allowed_page_usuario_nao_logado(client):
    """
    Realiza uma requisição na página de permissão negada de newsletter com usuário não logado.
    """
    response = client.get(reverse('newsletter:nao_permitido'))
    return response


@pytest.fixture
def resp_not_allowed_news_page_usuario_logado(client_usuario_logado):
    """
    Realiza uma requisição na página de permissão negada de newsletter com usuário logado.
    """
    response = client_usuario_logado.get(reverse('newsletter:nao_permitido'))
    return response


def test_redirect_not_allowed_page(resp_not_allowed_page_usuario_nao_logado):
    """
    Certifica de que o usuário não logado não acessa a página de acesso não permitido e é
    redirecionado para a página de login.
    """
    assert resp_not_allowed_page_usuario_nao_logado.status_code == 302
    assert resp_not_allowed_page_usuario_nao_logado.url.startswith('/accounts/login/')


def test_status_code_not_allowed_page(resp_not_allowed_news_page_usuario_logado):
    """
    Certifica de que o usuário logado acessa a página de acesso não permitido referente à newsletters.
    """
    assert resp_not_allowed_news_page_usuario_logado.status_code == 200


def test_nome_usuario_not_allowed_page(resp_not_allowed_news_page_usuario_logado, usuario_senha_plana):
    """
    Certifica de que o nome do usuário está presente na página de acesso não permitido
    referente à newsletters.
    """
    assert_contains(resp_not_allowed_news_page_usuario_logado, usuario_senha_plana.first_name)
