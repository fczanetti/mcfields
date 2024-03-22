import pytest
from django.urls import reverse

from mcfields.django_assertions import assert_contains


@pytest.fixture
def resp_pag_polit_privacidade(client):
    """
    Realiza uma requisição na página de política de privacidade.
    """
    resp = client.get(reverse('base:politica_privacidade'))
    return resp


def test_status_code_pag_politica_privac(resp_pag_polit_privacidade):
    """
    Certifica de que a página de política de privacidade é carregada com sucesso.
    """
    assert resp_pag_polit_privacidade.status_code == 200


def test_titulo_pag_politica_privac(resp_pag_polit_privacidade):
    """
    Certifica de que o título da página de política de privacidade está presente e correto.
    """
    assert_contains(resp_pag_polit_privacidade, "<title>McField's - Política de Privacidade</title>")
