import pytest
from django.urls import reverse

from mcfields.django_assertions import assert_contains


@pytest.fixture
def resp_sobre(client):
    """
    Cria uma requisição na página "sobre".
    """
    response = client.get(reverse('base:sobre'))
    return response


def test_status_code_sobre(resp_sobre):
    """
    Certifica de que a página "sobre" é carregada com sucesso.
    """
    assert resp_sobre.status_code == 200


def test_titulo_pagina_sobre(resp_sobre):
    """
    Certifica de que o título da página 'sobre a empresa' está presente e correto.
    """
    assert_contains(resp_sobre, "<title>McField's - Sobre</title>")
